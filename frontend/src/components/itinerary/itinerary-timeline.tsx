import React from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { MapPin, Sun, Coffee, Sunset, Moon } from 'lucide-react'
import type { ItineraryDay } from '@/types'

interface ItineraryTimelineProps {
  days: ItineraryDay[]
}

const timeIcons = {
  morning: Sun,
  afternoon: Coffee,
  evening: Sunset,
  night: Moon,
} as const

const timeColors = {
  morning: 'text-amber-500 bg-amber-50',
  afternoon: 'text-orange-500 bg-orange-50',
  evening: 'text-indigo-500 bg-indigo-50',
  night: 'text-blue-600 bg-blue-50',
} as const

export function ItineraryTimeline({ days }: ItineraryTimelineProps) {
  return (
    <div className="space-y-6">
      {days.map((day, di) => (
        <motion.div
          key={day.day}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: di * 0.15, duration: 0.4 }}
        >
          <Card className="overflow-hidden border-l-4 border-l-primary">
            <div className="bg-gradient-to-r from-primary/5 to-transparent px-5 py-3">
              <div className="flex items-center gap-2">
                <Badge variant="default" className="rounded-full">
                  Day {day.day}
                </Badge>
                <span className="text-sm font-medium text-text">{day.date}</span>
              </div>
              <p className="mt-1 flex items-center gap-1 text-xs text-text-muted">
                <MapPin className="h-3 w-3" />
                {day.location}
              </p>
            </div>

            <CardContent className="p-5">
              <div className="relative space-y-4">
                {day.activities.map((activity, ai) => (
                  <div key={ai} className="relative flex gap-4">
                    <div className="flex flex-col items-center">
                      <div
                        className={`flex h-8 w-8 items-center justify-center rounded-full ${
                          timeColors[activity.time as keyof typeof timeColors] || 'bg-surface-alt text-text-muted'
                        }`}
                      >
                        {React.createElement(
                          timeIcons[activity.time as keyof typeof timeIcons] || Sun,
                          { className: 'h-4 w-4' }
                        )}
                      </div>
                      {ai < day.activities.length - 1 && (
                        <div className="mt-1 h-full w-px bg-border" />
                      )}
                    </div>

                    <div className="flex-1 pb-4">
                      <p className="text-xs text-text-muted font-medium uppercase tracking-wider">
                        {activity.time}
                      </p>
                      <p className="mt-0.5 text-sm font-medium text-text">{activity.title}</p>
                      {activity.description && (
                        <p className="mt-1 text-xs text-text-secondary">{activity.description}</p>
                      )}
                      <div className="mt-1.5 flex gap-3 text-xs text-text-muted">
                        {activity.duration && <span>{activity.duration}</span>}
                        {activity.fee && <span>{activity.fee}</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
