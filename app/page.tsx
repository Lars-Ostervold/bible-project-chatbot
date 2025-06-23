'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'

export default function RedirectPage() {
  const [countdown, setCountdown] = useState(5)
  const redirectUrl = 'https://www.baptizedtechnology.com/chatbots/bibleproject'

  useEffect(() => {
    // Start countdown
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          window.location.href = redirectUrl
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [redirectUrl])

  const handleManualRedirect = () => {
    window.location.href = redirectUrl
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
            <svg
              className="w-8 h-8 text-blue-600 dark:text-blue-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            We've Moved!
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            The BibleProject AI chatbot has been updated and moved to a new location.
          </p>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            You'll be automatically redirected in{' '}
            <span className="font-bold text-blue-600 dark:text-blue-400 text-xl">
              {countdown}
            </span>{' '}
            seconds.
          </p>
        </div>

        <div className="space-y-4">
          <Button 
            onClick={handleManualRedirect}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
          >
            Take me there now
          </Button>
          
          <div className="text-sm text-gray-500 dark:text-gray-400">
            <p>If the automatic redirect doesn't work, click the button above or visit:</p>
            <a
              href={redirectUrl}
              className="text-blue-600 dark:text-blue-400 hover:underline break-all"
              target="_blank"
              rel="noopener noreferrer"
            >
              {redirectUrl}
            </a>
          </div>
        </div>
      </div>
    </div>
  )
} 