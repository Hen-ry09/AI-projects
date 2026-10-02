import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { MapPin, DollarSign, User, Calendar } from 'lucide-react'

export function ContextPanel() {
  return (
    <aside className="hidden xl:flex h-full w-80 flex-col border-l border-border bg-white p-4">
      <div className="space-y-5">
        <div>
          <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
            Current Trip
          </h2>
          <p className="mt-2 text-sm text-text-secondary">No active trip</p>
          <p className="text-xs text-text-muted mt-1">
            Start a conversation to build your itinerary
          </p>
        </div>

        <Separator />

        <div>
          <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">
            Traveler Profile
          </h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3 text-sm">
              <User className="h-4 w-4 text-text-muted" />
              <span className="text-text-secondary">Guest Traveler</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <Calendar className="h-4 w-4 text-text-muted" />
              <span className="text-text-secondary">Not specified</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <DollarSign className="h-4 w-4 text-text-muted" />
              <span className="text-text-secondary">Mid-range</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <MapPin className="h-4 w-4 text-text-muted" />
              <span className="text-text-secondary">Accra, Ghana</span>
            </div>
          </div>
        </div>

        <Separator />

        <div>
          <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">
            Quick Info
          </h2>
          <div className="flex flex-wrap gap-2">
            <Badge variant="default">Capital: Accra</Badge>
            <Badge variant="secondary">Currency: GHS</Badge>
            <Badge variant="accent">Language: English</Badge>
            <Badge variant="outline">Timezone: GMT+0</Badge>
          </div>
        </div>

        <Separator />

        <div>
          <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">
            Suggestions
          </h2>
          <div className="space-y-2">
            {[
              'Plan a 3-day Accra trip',
              'Find budget hotels in Kumasi',
              'Learn Twi greetings',
              'Best time to visit Mole',
            ].map((s) => (
              <Card key={s} className="cursor-pointer hover:bg-surface-alt transition-colors">
                <CardContent className="p-3">
                  <p className="text-xs text-text-secondary">{s}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </aside>
  )
}
