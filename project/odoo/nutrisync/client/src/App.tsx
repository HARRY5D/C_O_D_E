import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { ThemeProvider } from "./components/ui/theme-provider"
import { Toaster } from "./components/ui/toaster"
import { AuthProvider } from "./contexts/AuthContext"
import { Login } from "./pages/Login"
import { Register } from "./pages/Register"
import { ForgotPassword } from "./pages/ForgotPassword"
import { Layout } from "./components/Layout"
import { Dashboard } from "./pages/Dashboard"
import { MentalHealth } from "./pages/MentalHealth"
import { Fitness } from "./pages/Fitness"
import { Contact } from "./pages/Contact"
import { Appointments } from "./pages/Appointments"
import { Meditation } from "./pages/Meditation"
import { Metrics } from "./pages/Metrics"
import { Profile } from "./pages/Profile"
import { Integrations } from "./pages/Integrations"
import { ProtectedRoute } from "./components/ProtectedRoute"
import { FlutterApp } from "flutter"

function App() {
  return (
    <AuthProvider>
      <ThemeProvider defaultTheme="light" storageKey="ui-theme">
        <FlutterApp>
          <Router>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<Dashboard />} />
                <Route path="mental-health" element={<MentalHealth />} />
                <Route path="fitness" element={<Fitness />} />
                <Route path="contact" element={<Contact />} />
                <Route path="appointments" element={<Appointments />} />
                <Route path="meditation" element={<Meditation />} />
                <Route path="metrics" element={<Metrics />} />
                <Route path="profile" element={<Profile />} />
                <Route path="integrations" element={<Integrations />} />
              </Route>
            </Routes>
            <Toaster />
          </Router>
        </FlutterApp>
      </ThemeProvider>
    </AuthProvider>
  )
}

export default App
