import { motion } from 'framer-motion'
import { Avatar } from '@/components/ui/avatar'
import { MarkdownRenderer } from '@/components/chat/markdown-renderer'
import type { Message } from '@/types'

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className={`flex gap-4 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <Avatar
        fallback={isUser ? 'You' : 'AA'}
        className={isUser ? 'bg-primary/10 text-primary' : 'bg-secondary/10 text-secondary'}
      />

      <div
        className={`flex-1 max-w-[85%] md:max-w-[75%] ${
          isUser ? 'flex justify-end' : ''
        }`}
      >
        <div
          className={`rounded-2xl px-5 py-3.5 ${
            isUser
              ? 'bg-gradient-to-br from-primary to-primary-dark text-white rounded-tr-md'
              : 'bg-white border border-border text-text rounded-tl-md shadow-xs'
          }`}
        >
          {isUser ? (
            <p className="text-sm leading-relaxed">{message.content}</p>
          ) : (
            <div className="prose-custom">
              <MarkdownRenderer content={message.content} />
            </div>
          )}
        </div>
        <p className={`text-xs text-text-muted mt-1.5 ${isUser ? 'text-right' : ''}`}>
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </motion.div>
  )
}
