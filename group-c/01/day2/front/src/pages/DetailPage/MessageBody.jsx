import ReactMarkdown from 'react-markdown'
import rehypeSanitize from 'rehype-sanitize'
import rehypeRaw from 'rehype-raw'
import { Typography } from 'antd'

export default function MessageBody({ body, contentFormat }) {
  if (!body) return <Typography.Text type="secondary">暂无正文内容</Typography.Text>

  if (contentFormat === 'markdown') {
    return (
      <div className="message-body-md">
        <ReactMarkdown rehypePlugins={[rehypeRaw, rehypeSanitize]}>
          {body}
        </ReactMarkdown>
      </div>
    )
  }

  if (contentFormat === 'html') {
    return (
      <div
        className="message-body-html"
        dangerouslySetInnerHTML={{ __html: body }}
      />
    )
  }

  return (
    <Typography.Paragraph style={{ whiteSpace: 'pre-wrap' }}>
      {body}
    </Typography.Paragraph>
  )
}
