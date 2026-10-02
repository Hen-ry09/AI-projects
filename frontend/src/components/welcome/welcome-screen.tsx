import { motion } from 'framer-motion'
import { Compass, Sparkles } from 'lucide-react'
import { SuggestedPrompts } from '@/components/chat/suggested-prompts'

const prompts = [
  { title: 'Plan a 5-day trip to Ghana', prompt: 'Plan a 5-day trip to Ghana visiting Accra and Cape Coast' },
  { title: 'Recommend historical places', prompt: 'What are the best historical sites to visit in Ghana?' },
  { title: 'Teach me Twi phrases', prompt: 'Teach me some useful Twi phrases for traveling in Ghana' },
  { title: 'Create a budget itinerary', prompt: 'Create a 7-day budget itinerary for Ghana' },
  { title: 'Discover beaches near Accra', prompt: 'What are the best beaches near Accra?' },
]

interface WelcomeScreenProps {
  onSelectPrompt: (prompt: string) => void
}

export function WelcomeScreen({ onSelectPrompt }: WelcomeScreenProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="flex flex-col items-center justify-center min-h-full px-4 py-16"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.5 }}
        className="mb-8"
      >
        <div className="relative">
          <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-dark shadow-lg">
            <Compass className="h-10 w-10 text-white" />
          </div>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.6, type: 'spring', stiffness: 300 }}
            className="absolute -top-1 -right-1"
          >
            <Sparkles className="h-5 w-5 text-secondary" />
          </motion.div>
        </div>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="text-3xl font-bold text-text tracking-tight"
      >
        Akwaaba AI
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="mt-2 text-base text-text-secondary"
      >
        Your Intelligent Ghana Travel Companion
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="mt-10 w-full max-w-lg"
      >
        <SuggestedPrompts prompts={prompts} onSelect={onSelectPrompt} />
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7, duration: 0.5 }}
        className="mt-10 text-xs text-text-muted text-center max-w-md"
      >
        Ask me about destinations, culture, language, itineraries, budgets, and more.
        Powered by AI to help you discover the beauty of Ghana.
      </motion.p>
    </motion.div>
  )
}
