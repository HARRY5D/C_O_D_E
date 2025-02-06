import { Outlet } from "react-router-dom"
import { Header } from "./Header"
import { Footer } from "./Footer"
import { Sidebar } from "./Sidebar"

export function Layout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary">
      <Header />
      <div className="flex">
        <Sidebar />
        <div className="flex flex-col flex-1 lg:pl-72">
          <main className="flex-1 p-8 pt-16">
            <div className="mx-auto max-w-7xl">
              <Outlet />
            </div>
          </main>
          <Footer />
        </div>
      </div>
    </div>
  )
}