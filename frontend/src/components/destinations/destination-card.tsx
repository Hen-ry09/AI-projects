import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { MapPin, Clock, DollarSign, Star } from 'lucide-react'
import type { Destination } from '@/types'

interface DestinationCardProps {
  destination: Destination
  index: number
}

export function DestinationCard({ destination, index }: DestinationCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
    >
      <Card className="group overflow-hidden hover:shadow-md transition-all duration-300">
        <div className="relative h-40 bg-gradient-to-br from-primary/10 to-primary-dark/20 overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center">
            <MapPin className="h-8 w-8 text-primary/30" />
          </div>
          <div className="absolute bottom-3 left-3 flex gap-2">
            {destination.category.map((cat) => (
              <Badge key={cat} variant="default" className="capitalize">
                {cat}
              </Badge>
            ))}
          </div>
          <div className="absolute top-3 right-3 flex items-center gap-1 rounded-full bg-white/90 px-2 py-1 text-xs font-medium text-text shadow-xs">
            <Star className="h-3 w-3 text-secondary fill-secondary" />
            {destination.rating}
          </div>
        </div>

        <CardContent className="p-4">
          <h3 className="font-semibold text-text group-hover:text-primary transition-colors">
            {destination.name}
          </h3>
          <p className="mt-1 text-xs text-text-muted flex items-center gap-1">
            <MapPin className="h-3 w-3" />
            {destination.city}, {destination.region}
          </p>
          <p className="mt-2 text-xs text-text-secondary line-clamp-2 leading-relaxed">
            {destination.description}
          </p>
          <div className="mt-3 flex items-center gap-4 text-xs text-text-muted">
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {destination.duration}
            </span>
            <span className="flex items-center gap-1">
              <DollarSign className="h-3 w-3" />
              {destination.entryFee}
            </span>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
