import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import {
  Compass,
  Map,
  Heart,
  Clock,
  Settings,
  Plus,
  type LucideIcon,
} from 'lucide-react'

interface NavItem {
  icon: LucideIcon
  label: string
  active?: boolean
}

const navItems: NavItem[] = [
  { icon: Compass, label: 'New Trip', active: true },
  { icon: Map, label: 'Saved Trips' },
  { icon: Heart, label: 'Favorites' },
  { icon: Clock, label: 'History' },
]

export function Sidebar() {
  return (
    <aside className="flex h-full w-64 flex-col bg-sidebar text-sidebar-text">
      <div className="flex items-center gap-3 px-5 pt-6 pb-4">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary shadow-sm">
          <Compass className="h-5 w-5 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-semibold text-white">Akwaaba AI</h1>
          <p className="text-xs text-sidebar-text/60">Travel Companion</p>
        </div>
      </div>

      <Separator className="mx-4 bg-white/5" />

      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map((item) => (
          <Button
            key={item.label}
            variant={item.active ? 'sidebar-active' : 'sidebar'}
            size="default"
          >
            <item.icon className="h-4 w-4 shrink-0" />
            <span>{item.label}</span>
          </Button>
        ))}
      </nav>

      <Separator className="mx-4 bg-white/5" />

      <div className="p-3">
        <Button variant="sidebar" size="default">
          <Settings className="h-4 w-4 shrink-0" />
          <span>Settings</span>
        </Button>
      </div>

      <div className="px-3 pb-4">
        <Button
          variant="secondary"
          size="default"
          className="w-full gap-2 rounded-lg"
        >
          <Plus className="h-4 w-4" />
          New Trip
        </Button>
      </div>
    </aside>
  )
}
