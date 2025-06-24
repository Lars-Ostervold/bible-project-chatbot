import { redirect } from 'next/navigation'

export const metadata = {
  title: 'BibleProject AI'
}

export default function IndexPage() {
  // Redirect to main page since this is just a redirect site
  redirect('/')
}
