import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ArrowUp, Square } from 'lucide-react'

interface ChatInputProps {
  onSend: (message: string) => void
  isLoading: boolean
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSubmit = () => {
    if (!input.trim() || isLoading) return
    onSend(input.trim())
    setInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-border bg-white px-4 py-4">
      <div className="mx-auto max-w-3xl">
        <div className="relative flex items-end gap-2 rounded-2xl border border-border bg-surface-alt px-4 py-3 focus-within:border-primary/40 focus-within:shadow-xs transition-all duration-200">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about Ghana..."
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm text-text outline-none placeholder:text-text-muted max-h-[200px]"
          />

          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={handleSubmit}
            disabled={!input.trim() || isLoading}
            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-primary text-white transition-all duration-200 hover:bg-primary-light disabled:opacity-30 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Square className="h-4 w-4" />
            ) : (
              <ArrowUp className="h-4 w-4" />
            )}
          </motion.button>
        </div>
        <p className="mt-2 text-center text-xs text-text-muted">
          Akwaaba AI may produce inaccurate information. Verify key details.
        </p>
      </div>
    </div>
  )
}
