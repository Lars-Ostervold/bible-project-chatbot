import * as React from 'react'
import Link from 'next/link'
import Image from 'next/image'

export function Header() {
  return (
    <header className="sticky top-0 z-50 flex items-center justify-between w-full h-16 px-4 border-b shrink-0 bg-gradient-to-b from-background/10 via-background/50 to-background/80 backdrop-blur-xl">
      <div className="flex items-center">
        <Link href="/" className="text-sm font-medium">
          Home
        </Link>
      </div>
      <div className="flex items-center justify-center">
        <div className='flex items-center w-4/5 sm:w-1/3'>
          <Image
            src="/ask-bp-ai-logo.png"
            alt="Logo"
            width={500}
            height={500}
          />
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <Link href="/about" className="text-sm font-medium">
          About
        </Link>
        <Link href="/contact" className="text-sm font-medium">
          Contact
        </Link>
      </div>
    </header>
  )
}