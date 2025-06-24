import { redirect } from 'next/navigation'
import { type Metadata } from 'next'

export interface ChatPageProps {
  params: {
    id: string
  }
}

export async function generateMetadata({
  params
}: ChatPageProps): Promise<Metadata> {
  return {
    title: 'BibleProject AI - Redirecting'
  }
}

export default function ChatPage({ params }: ChatPageProps) {
  // Redirect to main page since this is just a redirect site
  redirect('/')
}
