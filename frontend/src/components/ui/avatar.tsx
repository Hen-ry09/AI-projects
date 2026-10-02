import * as React from 'react'
import { cn } from '@/lib/utils'

interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  fallback: string
}

const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, fallback, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'relative flex h-9 w-9 shrink-0 overflow-hidden rounded-full items-center justify-center bg-primary/10 text-primary font-semibold text-sm',
          className
        )}
        {...props}
      >
        <span>{fallback}</span>
      </div>
    )
  }
)
Avatar.displayName = 'Avatar'

export { Avatar }
