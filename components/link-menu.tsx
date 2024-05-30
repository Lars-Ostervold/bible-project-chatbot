'use client'
import * as React from 'react'
import Link from 'next/link'

export function DropdownMenu() {
  const [isOpen, setIsOpen] = React.useState(false)
  const buttonRef = React.useRef<HTMLButtonElement>(null);
  const menuRef = React.useRef<HTMLDivElement>(null);

  const toggleMenu = () => {
    setIsOpen(!isOpen)
  }

  // Close the dropdown when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
        const targetNode = event.target as Node
        if (isOpen && buttonRef.current && !buttonRef.current.contains(targetNode) && menuRef.current && !menuRef.current.contains(targetNode)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

return (
    <div className="relative">
      <button ref={buttonRef} onClick={toggleMenu} className="flex items-center justify-end space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="size-6">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`size-6 transition-transform duration-500 ${isOpen ? 'rotate-180' : ''}`}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {isOpen && (
        <div ref={menuRef} className="absolute right-0 mt-2 w-48 rounded-md shadow-lg ring-1 bg-white dark:bg-zinc-800 ring-black">
          <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
            <Link href="/about" className="block px-4 py-2 text-sm hover:bg-zinc-200 dark:hover:bg-zinc-600">About Us</Link>
            <Link href="/contact" className="block px-4 py-2 text-sm hover:bg-zinc-200 dark:hover:bg-zinc-600">Contact Us</Link>
            <Link href="https://buy.stripe.com/4gw00c3q41Tl0sU7ss" className="block px-4 py-2 text-sm hover:bg-zinc-200 dark:hover:bg-zinc-600">Support Us</Link>
          </div>
        </div>
      )}
    </div>
)
}