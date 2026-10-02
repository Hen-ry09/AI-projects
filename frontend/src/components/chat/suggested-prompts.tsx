import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'
import type { SuggestedPrompt } from '@/types'

interface SuggestedPromptsProps {
  prompts: SuggestedPrompt[]
  onSelect: (prompt: string) => void
}

export function SuggestedPrompts({ prompts, onSelect }: SuggestedPromptsProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {prompts.map((item, i) => (
        <motion.button
          key={item.title}
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 + i * 0.08, duration: 0.4, ease: 'easeOut' }}
          onClick={() => onSelect(item.prompt)}
          className="group flex items-start gap-3 rounded-xl border border-border bg-white p-4 text-left text-sm hover:border-primary/30 hover:shadow-xs hover:bg-primary/5 transition-all duration-200 cursor-pointer"
        >
          <div className="flex-1 min-w-0">
            <p className="font-medium text-text truncate">{item.title}</p>
          </div>
          <ArrowRight className="mt-0.5 h-4 w-4 shrink-0 text-text-muted group-hover:text-primary transition-colors" />
        </motion.button>
      ))}
    </div>
  )
}
