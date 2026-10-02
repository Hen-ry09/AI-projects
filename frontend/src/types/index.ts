export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

export interface Destination {
  id: string
  name: string
  city: string
  region: string
  category: string[]
  description: string
  entryFee: string
  duration: string
  rating: number
  imageUrl?: string
}

export interface ItineraryDay {
  day: number
  date: string
  location: string
  activities: ItineraryActivity[]
}

export interface ItineraryActivity {
  time: string
  title: string
  description?: string
  duration?: string
  fee?: string
}

export interface SuggestedPrompt {
  title: string
  prompt: string
}
