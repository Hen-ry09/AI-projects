import { useState, useRef, useEffect } from 'react'
import { Sidebar } from '@/components/layout/sidebar'
import { ContextPanel } from '@/components/layout/context-panel'
import { WelcomeScreen } from '@/components/welcome/welcome-screen'
import { ChatMessage } from '@/components/chat/chat-message'
import { ChatInput } from '@/components/chat/chat-input'
import { useChat } from '@/hooks/use-chat'
import { Menu } from 'lucide-react'

function App() {
  const { messages, isLoading, sendMessage } = useChat()
  const [showWelcome, setShowWelcome] = useState(true)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = (content: string) => {
    setShowWelcome(false)
    sendMessage(content)
  }

  return (
    <div className="flex h-screen bg-surface">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 lg:relative lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <Sidebar />
      </div>

      {/* Main area */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Header bar (mobile) */}
        <div className="flex items-center justify-between border-b border-border bg-white px-4 py-3 lg:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="rounded-lg p-2 hover:bg-surface-alt transition-colors cursor-pointer"
          >
            <Menu className="h-5 w-5 text-text" />
          </button>
          <h1 className="text-sm font-semibold text-text">Akwaaba AI</h1>
          <div className="w-9" />
        </div>

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto">
          {showWelcome ? (
            <WelcomeScreen onSelectPrompt={handleSend} />
          ) : (
            <div className="mx-auto max-w-3xl space-y-6 px-4 py-8">
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex items-center gap-3 px-4 py-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-full bg-secondary/10">
                    <span className="text-xs font-semibold text-secondary">AA</span>
                  </div>
                  <div className="flex gap-1.5">
                    <span className="h-2 w-2 animate-bounce rounded-full bg-primary/40 [animation-delay:0ms]" />
                    <span className="h-2 w-2 animate-bounce rounded-full bg-primary/40 [animation-delay:150ms]" />
                    <span className="h-2 w-2 animate-bounce rounded-full bg-primary/40 [animation-delay:300ms]" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>

      {/* Right context panel */}
      <ContextPanel />
    </div>
  )
}

export default App
