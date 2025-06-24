'use server'

export async function getMissingKeys() {
  // Return empty array since we don't need API keys for redirect
  return []
}

// Stub functions to prevent build errors from components that expect these
export async function getChats(userId?: string | null) {
  return []
}

export async function getSharedChat(id: string) {
  return null
}

export async function removeChat({ id, path }: { id: string; path: string }) {
  return { error: 'Not implemented' }
}

export async function shareChat(id: string) {
  return { error: 'Not implemented' }
}

export async function clearChats() {
  return { error: 'Not implemented' }
}
