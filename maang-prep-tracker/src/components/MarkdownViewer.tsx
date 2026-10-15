'use client'

import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Copy, Check, FileText } from 'lucide-react'

interface MarkdownViewerProps {
  content: string
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content }) => {
  const [copiedCode, setCopiedCode] = useState<string | null>(null)

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedCode(id)
    setTimeout(() => setCopiedCode(null), 2000)
  }

  if (!content) {
    return (
      <div className="py-16 text-center text-zinc-500 text-sm">
        <FileText className="w-8 h-8 mx-auto mb-2 text-zinc-600 opacity-60" />
        Select a phase doc or note to view its content.
      </div>
    )
  }

  return (
    <div className="markdown-body prose prose-invert max-w-none text-zinc-200 text-sm leading-relaxed space-y-4">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-2xl font-black text-white tracking-tight border-b border-zinc-800 pb-3 mt-6 mb-4">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-xl font-bold text-zinc-100 border-b border-zinc-800/80 pb-2 mt-6 mb-3">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-base font-semibold text-zinc-200 mt-5 mb-2">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-sm font-semibold text-zinc-300 mt-4 mb-2">
              {children}
            </h4>
          ),
          p: ({ children }) => (
            <p className="my-2 text-zinc-300 leading-relaxed text-sm">
              {children}
            </p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-outside pl-5 my-3 space-y-1 text-zinc-300">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-outside pl-5 my-3 space-y-1 text-zinc-300">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="leading-relaxed">{children}</li>
          ),
          blockquote: ({ children }) => {
            // Check for alert patterns in blockquotes
            const textContent = String(children)
            let borderColor = 'border-blue-500/40 bg-blue-500/5 text-blue-200'
            if (textContent.includes('[!NOTE]')) {
              borderColor = 'border-blue-500 bg-blue-950/20 text-blue-200'
            } else if (textContent.includes('[!TIP]')) {
              borderColor = 'border-emerald-500 bg-emerald-950/20 text-emerald-200'
            } else if (textContent.includes('[!IMPORTANT]')) {
              borderColor = 'border-purple-500 bg-purple-950/20 text-purple-200'
            } else if (textContent.includes('[!WARNING]')) {
              borderColor = 'border-amber-500 bg-amber-950/20 text-amber-200'
            } else if (textContent.includes('[!CAUTION]')) {
              borderColor = 'border-rose-500 bg-rose-950/20 text-rose-200'
            }

            return (
              <blockquote className={`border-l-4 pl-4 py-2 my-4 rounded-r-xl ${borderColor}`}>
                {children}
              </blockquote>
            )
          },
          table: ({ children }) => (
            <div className="overflow-x-auto my-4 rounded-xl border border-zinc-800">
              <table className="min-w-full divide-y divide-zinc-800 text-xs">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-zinc-900/90 text-zinc-200 font-semibold">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="px-3.5 py-2.5 text-left font-semibold text-zinc-300">{children}</th>
          ),
          td: ({ children }) => (
            <td className="px-3.5 py-2 border-t border-zinc-800/60 text-zinc-300">{children}</td>
          ),
          code: ({ inline, className, children, ...props }: React.ComponentPropsWithoutRef<'code'> & { inline?: boolean }) => {
            const match = /language-(\w+)/.exec(className || '')
            const codeString = String(children).replace(/\n$/, '')
            const codeId = Math.random().toString(36).substring(7)

            if (!inline && match) {
              return (
                <div className="relative my-4 rounded-xl overflow-hidden border border-zinc-800 bg-[#0d0e15]">
                  <div className="flex items-center justify-between px-3.5 py-1.5 bg-zinc-900/80 border-b border-zinc-800/80 text-[11px] font-mono text-zinc-400">
                    <span>{match[1]}</span>
                    <button
                      onClick={() => handleCopy(codeString, codeId)}
                      className="flex items-center gap-1 hover:text-white transition"
                    >
                      {copiedCode === codeId ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                          <span className="text-emerald-400">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="p-4 text-xs font-mono text-zinc-200 overflow-x-auto leading-relaxed">
                    <code>{children}</code>
                  </pre>
                </div>
              )
            }

            return (
              <code
                className="px-1.5 py-0.5 rounded bg-zinc-800/70 border border-zinc-700/50 text-blue-300 font-mono text-xs"
                {...props}
              >
                {children}
              </code>
            )
          },
          hr: () => <hr className="border-zinc-800 my-6" />,
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 underline underline-offset-2"
            >
              {children}
            </a>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
