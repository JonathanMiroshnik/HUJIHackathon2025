import { Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation/Navigation'
import MainPage from './pages/MainPage/MainPage'
import MemoryPage from './pages/MemoryPage/MemoryPage'

import './App.css'

function App() {
  return (
    <div className="app">
      <Navigation />
      <main className="main-style">
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/memory" element={<MemoryPage />} />
        </Routes>
      </main>      
    </div>
  )
}

export default App