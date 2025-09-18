import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_app/admin')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div className="flex flex-col justify-start w-full h-full">Hello "/_admin"!</div>
  )
}
