//import { useState } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from './assets/vite.svg'
//import heroImg from './assets/hero.png'
import './App.css'

import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Home from './pages/Home';
import EventList from './pages/EventList';
import Event from './pages/Event';

const router = createBrowserRouter([
  { path: '/', element: <Home /> },
  { path: '/eventlist', element: <EventList /> },
  { path: '/event', element: <Event /> }
])

function App() {
  return (
    <RouterProvider router={router} />
  )
}

export default App
