import * as React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import HomeRoundedIcon from '@mui/icons-material/HomeRounded'
import { IconSeparator } from '@/components/ui/icons'
import { DropdownMenu } from './link-menu'

function UserOrLogin() {
  return (
    <>
      <Link href="/new" rel="nofollow">
        <HomeRoundedIcon/>
      </Link>
      <div className="flex items-center">
        <IconSeparator className="size-6 text-muted-foreground/50" />
      </div>
    </>
  )
}

export function Header() {
  return (
    <header className="sticky top-0 z-50 flex items-center justify-between w-full h-16 px-4 border-b shrink-0 bg-gradient-to-b from-background/10 via-background/50 to-background/80 backdrop-blur-xl">
      <div className="flex items-center">
        <React.Suspense fallback={<div className="flex-1 overflow-auto" />}>
          <UserOrLogin />
        </React.Suspense>
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
      <div className="relative">
        <DropdownMenu />
      </div>
    </header>
  )
}