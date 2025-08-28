export const metadata = { 
  title: 'AI Path Advisor Pro', 
  description: 'Advanced learning path planner with ILP optimization' 
};

import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">{children}</div>
      </body>
    </html>
  )
}