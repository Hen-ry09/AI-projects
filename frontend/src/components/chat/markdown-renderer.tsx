interface MarkdownRendererProps {
  content: string
}

function parseMarkdown(text: string): React.ReactNode[] {
  const lines = text.split('\n')
  const elements: React.ReactNode[] = []
  let listItems: React.ReactNode[] = []
  let inTable = false
  let tableRows: React.ReactNode[] = []
  let listIndex = 0

  const flushList = () => {
    if (listItems.length > 0) {
      elements.push(
        <ul key={`ul-${listIndex}`} className="my-2 space-y-1">
          {listItems}
        </ul>
      )
      listItems = []
      listIndex++
    }
  }

  const flushTable = () => {
    if (tableRows.length > 0) {
      elements.push(
        <div key={`table-${listIndex}`} className="my-3 overflow-x-auto rounded-lg border border-border">
          <table className="min-w-full text-sm">
            {tableRows}
          </table>
        </div>
      )
      tableRows = []
      inTable = false
      listIndex++
    }
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]

    if (!line.trim()) {
      flushList()
      flushTable()
      continue
    }

    if (line.startsWith('| ')) {
      flushList()
      const cells = line.split('|').filter(Boolean).map(c => c.trim())

      if (line.includes('---')) {
        continue
      }

      if (!inTable) {
        inTable = true
        tableRows.push(
          <thead key={`thead-${i}`} className="bg-surface-alt">
            <tr>
              {cells.map((cell, ci) => (
                <th key={ci} className="px-4 py-2 text-left text-xs font-semibold uppercase text-text-secondary border-r last:border-r-0 border-border">
                  {cell.replace(/\*\*/g, '')}
                </th>
              ))}
            </tr>
          </thead>
        )
      } else {
        tableRows.push(
          <tr key={`tr-${i}`} className="border-t border-border hover:bg-surface-alt/50">
            {cells.map((cell, ci) => (
              <td key={ci} className="px-4 py-2 text-sm text-text-secondary border-r last:border-r-0 border-border">
                {cell}
              </td>
            ))}
          </tr>
        )
      }
      continue
    }

    if (line.startsWith('- ') || line.startsWith('* ')) {
      flushTable()
      const text = line.replace(/^[-*]\s+/, '')
      listItems.push(
        <li key={`li-${i}`} className="flex items-start gap-2 text-sm text-text-secondary">
          <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary/40" />
          <span>{renderInline(text)}</span>
        </li>
      )
      continue
    }

    if (/^\d+\.\s/.test(line)) {
      flushTable()
      const text = line.replace(/^\d+\.\s+/, '')
      listItems.push(
        <li key={`li-${i}`} className="flex items-start gap-2 text-sm text-text-secondary">
          <span className="mt-0.5 text-xs font-semibold text-primary shrink-0 w-4">
            {line.match(/^\d+/)?.[0]}
          </span>
          <span>{renderInline(text)}</span>
        </li>
      )
      continue
    }

    flushList()
    flushTable()

    if (line.startsWith('### ')) {
      elements.push(
        <h3 key={`h3-${i}`} className="mt-4 mb-2 text-base font-semibold text-text">
          {line.replace('### ', '')}
        </h3>
      )
    } else if (line.startsWith('## ')) {
      elements.push(
        <h2 key={`h2-${i}`} className="mt-5 mb-2 text-lg font-bold text-text">
          {line.replace('## ', '')}
        </h2>
      )
    } else if (line.startsWith('# ')) {
      elements.push(
        <h1 key={`h1-${i}`} className="mt-5 mb-3 text-xl font-bold text-text">
          {line.replace('# ', '')}
        </h1>
      )
    } else {
      elements.push(
        <p key={`p-${i}`} className="my-1.5 text-sm leading-relaxed text-text-secondary">
          {renderInline(line)}
        </p>
      )
    }
  }

  flushList()
  flushTable()

  return elements
}

function renderInline(text: string): React.ReactNode {
  const parts: React.ReactNode[] = []
  let remaining = text

  const regex = /(\*\*(.+?)\*\*|`(.+?)`)/g
  let lastIndex = 0
  let match: RegExpExecArray | null

  while ((match = regex.exec(remaining)) !== null) {
    if (match.index > lastIndex) {
      parts.push(remaining.slice(lastIndex, match.index))
    }

    if (match[2]) {
      parts.push(
        <strong key={`b-${match.index}`} className="font-semibold text-text">
          {match[2]}
        </strong>
      )
    } else if (match[3]) {
      parts.push(
        <code
          key={`code-${match.index}`}
          className="rounded bg-surface-alt px-1.5 py-0.5 text-xs font-mono text-accent"
        >
          {match[3]}
        </code>
      )
    }

    lastIndex = match.index + match[0].length
  }

  if (lastIndex < remaining.length) {
    parts.push(remaining.slice(lastIndex))
  }

  return parts.length > 0 ? <>{parts}</> : text
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const elements = parseMarkdown(content)

  return (
    <div className="space-y-1">
      {elements.map((el, i) => (
        <div key={i}>{el}</div>
      ))}
    </div>
  )
}
