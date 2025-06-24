import { redirect } from 'next/navigation'
import { type Metadata } from 'next'

export const runtime = 'edge'
export const preferredRegion = 'home'

interface SharePageProps {
  params: {
    id: string
  }
}

export async function generateMetadata({
  params
}: SharePageProps): Promise<Metadata> {
  return {
    title: 'BibleProject AI - Redirecting'
  }
}

export default function SharePage({ params }: SharePageProps) {
  // Redirect to main page since this is just a redirect site
  redirect('/')
}
