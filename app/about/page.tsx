import { ExternalLink } from '@/components/external-link'
export default function AboutPage() {
    return (
        <div className="flex justify-center">
            <div className="w-3/5">
                <main className="flex flex-col p-4">
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">How&apos;s it work?</h2>
                        <p className="mb-4">
                            The chatbot is what is called a &apos;retrival augmented generation&apos; (RAG) chatbot. Feel free to read up on it <ExternalLink href="https://huggingface.co/transformers/model_doc/rag.html">here</ExternalLink>. But here&apos;s the gist of how it works:
                        </p>
                        <ol className="mb-4 p-6">
                            <li className="mb-2">
                                1. You enter a question into the chatbot.
                            </li>
                            <li className="mb-2">
                                2. The chatbot takes your question and searches through a database of Bible Project content and finds the most relevants snippets.
                            </li>
                            <li className="mb-2">
                                3. We take those snippets, along with your question, and send it to ChatGPT. We ask ChatGPT to generate a response based on the snippets and your question.
                            </li>
                            <li className="mb-2">
                                4. We take the response from ChatGPT and send it back to you.
                            </li>
                        </ol>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Why did you build it?</h2>
                        <p className="mb-4">
                            We want people to have a reliable source that can quickly answer tough questions. 
                        </p>
                        <p>
                            Finding answers to tough questions is really hard. We&apos;ve found the Bible Project to have some of the best content out there for answering those questions. But it can be hard to find the right video or podcast episode. So this chatbot is a way to help find the right content, but also summarize lots of content into a short answer. However, becuase the chatbot wil almost always miss the nuance of the content, we hope that the &apos;teaser&apos; from the chatbot encourages people to become the Psalms 1 kind of Bible nerd, chewing on the Scriptures day and night.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Who made this thing?</h2>
                        <p className="mb-4">
                            The main infrastructure for this project was based on a <ExternalLink href="https://vercel.com/templates/next.js/nextjs-ai-chatbot"> chatbot template</ExternalLink> from Vercel. But the custom code was mostly made by a dude named <ExternalLink href="https://lars-ostervold.vercel.app/" >Lars</ExternalLink>. Though he also had help from some friends 😊.
                        </p>
                        <p>
                            We&apos;re always looking to make askBP better, so if you have any feedback or suggestions, feel free to reach out to us at <ExternalLink href="/contact">contact</ExternalLink>.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">User Data and Privacy</h2>
                        <p className="mb-4">
                            None of your data is harvested and made publicly available. The way it&apos;s set up, we can&apos;t even access it other than to display it for you (that&apos;s right, we even locked ourselves out! That&apos;s how good we are.) This means your questions, your passwords, and your answers are all safe and secure. You are the only one who will ever see them, unless you share them yourselves. 
                        </p>
                    </section>
                </main>
            </div>
        </div>
    );
}
