import { ExternalLink } from '@/components/external-link'
export default function PrivacyPolicyPage() {
    return (
        <div className="flex justify-center">
            <div className="w-full md:w-3/5">
                <main className="flex flex-col p-4">
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Introduction</h2>
                        <p>
                            This Privacy Policy describes how we handle any information you provide through our chatbot.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Information We Collect</h2>
                        <p>
                            We do not collect or store any personal information about you when you use our chatbot.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Third-Party Platforms</h2>
                        <p>
                            If our chatbot operates on a third-party platform (e.g., Vercel), that platform may collect information about your use of the chatbot according to their own privacy policies.  We recommend you review the privacy policies of any third-party platforms you use to access our chatbot.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Changes to Privacy Policy</h2>
                        <p>
                            We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new Privacy Policy here.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Contact Us</h2>
                        <p>
                            If you have any questions about this Privacy Policy, please <ExternalLink href="/contact"> contact us</ExternalLink>.
                        </p>
                    </section>
                </main>
            </div>
        </div>
    );
}