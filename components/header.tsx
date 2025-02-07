import * as React from 'react'
import Link from 'next/link'

import { auth } from '@/auth'
import { Button, buttonVariants } from '@/components/ui/button'
import {
  IconSeparator,
} from '@/components/ui/icons'
import { UserMenu } from '@/components/user-menu'
import { SidebarMobile } from './sidebar-mobile'
import { SidebarToggle } from './sidebar-toggle'
import { ChatHistory } from './chat-history'
import { Session } from '@/lib/types'
import Image from 'next/image'
import { DropdownMenu } from './link-menu'
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';

async function UserOrLogin() {
  const session = (await auth()) as Session
  return (
    <>
      {session?.user ? (
        <>
          <SidebarMobile>
            <ChatHistory userId={session.user.id} />
          </SidebarMobile>
          <SidebarToggle />
        </>
      ) : (
        <Link href="/new" rel="nofollow">
          <HomeRoundedIcon/>
        </Link>
      )}
      <div className="flex items-center">
        <IconSeparator className="size-6 text-muted-foreground/50" />
        {session?.user ? (
          <UserMenu user={session.user} />
        ) : (
          <Button variant="link" asChild className="-ml-2">
            {/* <Link href="/login">Login</Link> */}
          </Button>
        )}
      </div>
    </>
  )
}

export function Header() {
  const isSmallScreen = typeof window !== 'undefined' && window.innerWidth < 768;

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between w-full h-16 px-4 border-b shrink-0 bg-gradient-to-b from-background/10 via-background/50 to-background/80 backdrop-blur-xl">
      <div className="flex items-center">
        <React.Suspense fallback={<div className="flex-1 overflow-auto" />}>
          <UserOrLogin />
        </React.Suspense>
      </div>
      <div className="flex items-center justify-center">
        {/* Okay I've got no idea why this code worked to get the image to display well on both screens, but it did so no need to ask questions */}
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
  );
}