import 'server-only'

import {
  createAI,
  createStreamableUI,
  getMutableAIState,
  getAIState,
  render,
  createStreamableValue
} from 'ai/rsc'
import OpenAI from 'openai'

import {
  spinner,
  BotCard,
  BotMessage,
  SystemMessage,
  Stock,
  Purchase
} from '@/components/stocks'

import { z } from 'zod'
import { EventsSkeleton } from '@/components/stocks/events-skeleton'
import { Events } from '@/components/stocks/events'
import { StocksSkeleton } from '@/components/stocks/stocks-skeleton'
import { Stocks } from '@/components/stocks/stocks'
import { StockSkeleton } from '@/components/stocks/stock-skeleton'
import {
  formatNumber,
  runAsyncFnWithoutBlocking,
  sleep,
  nanoid
} from '@/lib/utils'
import { saveChat } from '@/app/actions'
import { SpinnerMessage, UserMessage } from '@/components/stocks/message'
import { Chat } from '@/lib/types'
import { auth } from '@/auth'
import { Pinecone } from '@pinecone-database/pinecone'
import { supabase } from '@/lib/supabaseClient'
import { SourceBlocks } from '@/components/source-blocks'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || ''
})
const embed_model = 'text-embedding-ada-002'

const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY || '' })
const index = pinecone.index('bible-project-index')
const CONDENSE_QUESTION_TEMPLATE = 'Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else.'

const sourcesToRender = 2

// We don't need the 'path' module, so we remove the import statement
// import path from 'path'
function getBaseName(filePath: string) {
  // Replace all backslashes with forward slashes
  filePath = filePath.replace(/\\/g, '/');

  // Split the file path into segments
  const segments = filePath.split('/');

  // Get the last segment, which should be the file name with extension
  const fileNameWithExtension = segments.pop();

  // Check if fileNameWithExtension is undefined
  if (!fileNameWithExtension) {
    throw new Error('Invalid file path');
  }

  // Split the file name into name and extension
  const fileNameParts = fileNameWithExtension.split('.');

  // Remove the extension part
  fileNameParts.pop();

  // Join the remaining parts back together
  const fileName = fileNameParts.join('.');

  return fileName;
}

async function confirmPurchase(symbol: string, price: number, amount: number) {
  'use server'

  const aiState = getMutableAIState<typeof AI>()

  const purchasing = createStreamableUI(
    <div className="inline-flex items-start gap-1 md:items-center">
      {spinner}
      <p className="mb-2">
        Purchasing {amount} ${symbol}...
      </p>
    </div>
  )

  const systemMessage = createStreamableUI(null)

  runAsyncFnWithoutBlocking(async () => {
    await sleep(1000)

    purchasing.update(
      <div className="inline-flex items-start gap-1 md:items-center">
        {spinner}
        <p className="mb-2">
          Purchasing {amount} ${symbol}... working on it...
        </p>
      </div>
    )

    await sleep(1000)

    purchasing.done(
      <div>
        <p className="mb-2">
          You have successfully purchased {amount} ${symbol}. Total cost:{' '}
          {formatNumber(amount * price)}
        </p>
      </div>
    )

    systemMessage.done(
      <SystemMessage>
        You have purchased {amount} shares of {symbol} at ${price}. Total cost ={' '}
        {formatNumber(amount * price)}.
      </SystemMessage>
    )

    aiState.done({
      ...aiState.get(),
      messages: [
        ...aiState.get().messages.slice(0, -1),
        {
          id: nanoid(),
          role: 'function',
          name: 'showStockPurchase',
          content: JSON.stringify({
            symbol,
            price,
            defaultAmount: amount,
            status: 'completed'
          })
        },
        {
          id: nanoid(),
          role: 'system',
          content: `[User has purchased ${amount} shares of ${symbol} at ${price}. Total cost = ${
            amount * price
          }]`
        }
      ]
    })
  })

  return {
    purchasingUI: purchasing.value,
    newMessage: {
      id: nanoid(),
      display: systemMessage.value
    }
  }
}

async function submitUserMessage(content: string): Promise<{ id: string, display: React.ReactNode, sources: string[] }> {
  'use server'

  const aiState = getMutableAIState<typeof AI>()
  aiState.update({
    ...aiState.get(),
    messages: [
      ...aiState.get().messages,
      {
        id: nanoid(),
        role: 'user',
        content,
      }
    ]
  })

  let search_text = content;
  let context = '';

  //Send the user message to the AI model to ask if it is on topic
  const lastUserMessage = aiState.get().messages[aiState.get().messages.length - 1]
  const on_topic_check_message = `Is the message below on topic for a Christian chatbot? Respond with either 'Yes.' or 'No.'\n\n${lastUserMessage.content}`;
  const completion = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{role: 'user', content: on_topic_check_message}],
  });
  if (completion.choices[0]?.message?.content === 'No.') {
    context = 'NO CONTEXT BECAUSE MESSAGE IS OFF TOPIC';
    var sources: any[] = []
  } else {
    //Check if the user message is the first message in the chat history
    const firstMessage = aiState.get().messages.length === 1

    //If not the first question, we need to generate a single query for the vector database
    if (!firstMessage) {
      //Store chat history (just role and content) in a list (chat_history)
      const chat_history = aiState.get().messages.map((message: any) => ({
        role: message.role,
        content: message.content
      }));
      // Add the condense prompt to the chat history so the LLM can generate a single query for the vector database
      const condense_prompt = { role: 'system', content: CONDENSE_QUESTION_TEMPLATE}
      chat_history.push(condense_prompt)
      const completion = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: chat_history,
      });
      const completionResponse = completion.choices[0]?.message?.content;
      if (!completionResponse) {
        throw new Error('Failed to retrieve completion response from completion');
      }
      search_text = completionResponse;
    }

    // Embed user message using OpenAI embeddings
    const embed = await openai.embeddings.create({
      input: [search_text],
      model: embed_model
    });

    // Retrieve from Pinecone
    const xq = embed.data[0].embedding;

    // Get relevant contexts (including the questions)
    const chunks = await index.query({ vector: xq, topK: 10, includeMetadata: true, includeValues: true});

    //Store each source in a list
    const source_file_name: string[] = []
    for (const chunk of chunks.matches) {
      if (chunk.metadata) {
        source_file_name.push(String(chunk.metadata.source))
      }
    }
    const baseNames = source_file_name.map(getBaseName)

    const { data, error } = await supabase
      .from('source-links')
      .select()
      .in('file_name', baseNames)
    const sourceMap = data

    var sources = sourceMap ? sourceMap.slice(0,sourcesToRender) : []

    //Store context chunks in user message, surround by tags '<context>' '</context>'
    for (const chunk of chunks.matches) {
      if (chunk.metadata) {
        context += chunk.metadata.text + '\n\n\n';
      }
    }
    context = '<context>\n' + context + '</context>';
  }


  let textStream: undefined | ReturnType<typeof createStreamableValue<string>>
  let textNode: undefined | React.ReactNode

  const ui = render({
    model: 'gpt-3.5-turbo',
    provider: openai,
    initial: <SpinnerMessage />,
    messages: [
      {
        role: 'system',
        content: `\
You are a chatbot that helps people explore Christianity using content from an organization called BibleProject.
You and the user can discuss themes, personal problems, difficult questions, and more.
You will answer according to the chat history and the context denoted by <context>string</context>. Do not hallucinate answers that are not in the context I provide.

Here is the context to answer the user's question:
${context}`
      },
      ...aiState.get().messages.map((message: any) => ({
        role: message.role,
        content: message.content,
        name: message.name
      }))
    ],
    text: ({ content, done, delta }) => {
      if (!textStream) {
        textStream = createStreamableValue('')
        textNode = <BotMessage content={textStream.value} sources={sources}/>
      }

      if (done) {
        textStream.done()
        aiState.done({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages,
            {
              id: nanoid(),
              role: 'assistant',
              content,
              sources: sources
            }
          ]
        })
      } else {
        textStream.update(delta)
      }

      return textNode
    }
  })

  return {
    id: nanoid(),
    display: ui,
    sources: sources
  }
}

type Source = {
  file_name: string;
  link: string;
  title: string;
  type_of_media: string;
  thumbnail_url: string;
}

export type Message = {
  role: 'user' | 'assistant' | 'system' | 'function' | 'data' | 'tool'
  content: string
  id: string
  name?: string,
  sources?: Source[]
}

export type AIState = {
  chatId: string
  messages: Message[]
}

export type UIState = {
  id: string
  display: React.ReactNode
}[]



export const AI = createAI<AIState, UIState>({
  actions: {
    submitUserMessage,
    confirmPurchase
  },
  initialUIState: [],
  initialAIState: { chatId: nanoid(), messages: [] },
  onGetUIState: async () => {
    'use server'

    const session = await auth()

    if (session && session.user) {
      const aiState = getAIState()

      if (aiState) {
        const uiState = getUIStateFromAIState(aiState)
        return uiState
      }
    } else {
      return
    }
  },
  onSetAIState: async ({ state, done }) => {
    'use server'

    const session = await auth()

    if (session && session.user) {
      const { chatId, messages } = state

      const createdAt = new Date()
      const userId = session.user.id as string
      const path = `/chat/${chatId}`
      const title = messages[0].content.substring(0, 100)

      const chat: Chat = {
        id: chatId,
        title,
        userId,
        createdAt,
        messages,
        path
      }

      await saveChat(chat)
    } else {
      return
    }
  }
})

export const getUIStateFromAIState = (aiState: Chat) => {
  return aiState.messages
    .filter(message => message.role !== 'system')
    .map((message, index) => ({
      id: `${aiState.chatId}-${index}`,
      display:
        message.role === 'function' ? (
          message.name === 'listStocks' ? (
            <BotCard>
              <Stocks props={JSON.parse(message.content)} />
            </BotCard>
          ) : message.name === 'showStockPrice' ? (
            <BotCard>
              <Stock props={JSON.parse(message.content)} />
            </BotCard>
          ) : message.name === 'showStockPurchase' ? (
            <BotCard>
              <Purchase props={JSON.parse(message.content)} />
            </BotCard>
          ) : message.name === 'getEvents' ? (
            <BotCard>
              <Events props={JSON.parse(message.content)} />
            </BotCard>
          ) : null
        ) : message.role === 'user' ? (
          <UserMessage>{message.content}</UserMessage>
        ) : (
          <BotMessage content={message.content} sources={message?.sources || []}  />
        )
    }))
}
 