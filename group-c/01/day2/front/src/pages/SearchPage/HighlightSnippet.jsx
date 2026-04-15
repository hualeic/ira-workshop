export default function HighlightSnippet({ html }) {
  if (!html) return null
  return (
    <div
      style={{
        fontSize: 13,
        color: '#666',
        background: '#fafafa',
        padding: '4px 8px',
        borderRadius: 4,
        marginTop: 4,
      }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
