import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import TodoList from './pages/TodoList'
import CreateTodo from './pages/CreateTodo'
import EditTodo from './pages/EditTodo'
import CreateTag from './pages/CreateTag'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/todos" element={<TodoList />} />
        <Route path="/create-todo" element={<CreateTodo />} />
        <Route path="/edit-todo/:id" element={<EditTodo />} />
        <Route path="/create-tag" element={<CreateTag />} />
        <Route path="/" element={<Navigate to="/todos" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
