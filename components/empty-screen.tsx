import { UseChatHelpers } from 'ai/react'

import { Button } from '@/components/ui/button'
import { ExternalLink } from '@/components/external-link'
import { IconArrowRight } from '@/components/ui/icons'

const exampleMessages = [
  {
    heading: 'Explain technical concepts',
    message: `What is a "serverless function"?`
  },
  {
    heading: 'Summarize an article',
    message: 'Summarize the following article for a 2nd grader: \n'
  },
  {
    heading: 'Draft an email',
    message: `Draft an email to my boss about the following: \n`
  }
]

export function EmptyScreen() {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="flex flex-col gap-2 rounded-lg border bg-background p-8">
        <h1 className="text-base sm:text-lg font-semibold">
          Welcome to BibleProject - Ask AI!
        </h1>
        <p className="text-sm sm:text-base leading-normal text-muted-foreground">
          This is an is an AI-powered chat interface that can help you with explore the Bible as a unified story that leads to Jesus.

          We hope this chatbout can give you quick answers to your questions and that it sparks a curiosity to dive deeper.
        </p>
        <p className="text-sm sm:text-base leading-normal text-muted-foreground">
          We are still in the beta phase, so we would love to hear your feedback! Please try it out and give us your thoughts <ExternalLink href="/contact">here</ExternalLink>.
        </p>
        <h2 className="text-sm sm:text-md font-semibold">
          We are not affiliated with BibleProject. Do not take these answers as official BibleProject content. Always check the original source.
        </h2>
      </div>
    </div>
  )
}