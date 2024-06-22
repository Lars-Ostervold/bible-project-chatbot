import { ExternalLink } from '@/components/external-link'

export default function TermsOfServicePage() {
    return (
        <div className="flex justify-center">
            <div className="w-full sm:w-3/5">
                <main className="flex flex-col p-4">
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Agreement to Terms</h2>
                        <p className="mb-4">
                            By using this chatbot, you agree to these Terms of Service (&quot;Terms&quot;). If you disagree with any part of the Terms, then you may not use the chatbot.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Acceptable Use</h2>
                        <p className="mb-4">
                            You agree to use the chatbot only for lawful purposes and in a way that does not violate the rights of any other person or entity. You agree not to use the chatbot for any of the following purposes:
                        </p>
                        <ul className="mb-4 p-6">
                            <li className="mb-2">To transmit any content that is unlawful, harmful, threatening, abusive, harassing, defamatory, vulgar, obscene, hateful, or racially or ethnically offensive.</li>
                            <li className="mb-2">To impersonate any person or entity, or to falsely state or otherwise misrepresent your affiliation with a person or entity.</li>
                            <li className="mb-2">To interfere with the operation of the chatbot or any servers or networks connected to the chatbot.</li>
                            <li className="mb-2">To upload viruses or other malicious code that could damage or interfere with the chatbot or any other system or network.</li>
                            <li className="mb-2">To attempt to gain unauthorized access to the chatbot, other accounts, computer systems or networks connected to the chatbot, through hacking, password mining or other means.</li>
                        </ul>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Disclaimers</h2>
                        <p className="mb-4">
                            The chatbot is provided &quot;as is&quot; and without warranty of any kind, express or implied. The operator of the chatbot disclaims all warranties, including any implied warranties of merchantability, fitness for a particular purpose, title, and non-infringement.
                        </p>
                        <p>
                            The operator of the chatbot does not warrant that the chatbot will be uninterrupted or error-free, that defects will be corrected, or that the chatbot or the server that makes it available are free of viruses or other harmful components.
                        </p>
                        <p>
                            The operator of the chatbot does not warrant or make any representations regarding the use or the results of the use of the materials in the chatbot in terms of their correctness, accuracy, reliability, or otherwise.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Limitation of Liability</h2>
                        <p className="mb-4">
                            The operator of the chatbot shall not be liable for any damages arising out of or in connection with your use of the chatbot. This includes, but is not limited to, direct, indirect, incidental, consequential, special, or punitive damages.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Termination</h2>
                        <p className="mb-4">
                            The operator of the chatbot reserves the right to terminate your access to the chatbot at any time and for any reason, without notice.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Governing Law</h2>
                        <p className="mb-4">
                            These Terms shall be governed by and construed in accordance with the laws of [State where your business is located], without regard to its conflict of law provisions.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Updates to Terms of Service</h2>
                        <p className="mb-4">
                            The operator of the chatbot reserves the right to update these Terms at any time. We will notify you of any material changes by posting the new Terms on the chatbot. You are advised to review the Terms periodically for any changes.
                        </p>
                    </section>
                    <section className="mb-8">
                        <h2 className="text-2xl font-bold mb-2 text-center">Contact Us</h2>
                        <p className="mb-4">
                            If you have any questions about these Terms, please <ExternalLink href="/contact"> contact us</ExternalLink>.
                        </p>
                    </section>
                </main>
            </div>
        </div>
    );
}