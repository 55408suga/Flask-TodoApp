import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import Calendar from 'react-calendar';
import './Calendar.css';

const TodoList = () => {
    const [todos, setTodos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [search, setSearch] = useState('');
    const [user, setUser] = useState(null);
    const [viewMode, setViewMode] = useState('list'); // 'list' or 'calendar'
    const navigate = useNavigate();

    const fetchUser = async () => {
        try {
            const response = await api.get('/me');
            setUser(response.data);
        } catch (err) {
            console.error("Failed to fetch user");
        }
    };

    const fetchTodos = async (query = '') => {
        try {
            setLoading(true);
            const response = await api.get('/todos', {
                params: { name: query }
            });
            setTodos(response.data);
        } catch (err) {
            if (err.response && err.response.status === 401) {
                navigate('/login');
            } else {
                setError(err.message);
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();
        fetchTodos();
    }, []);

    const handleLogout = async () => {
        try {
            await api.post('/logout');
            navigate('/login');
        } catch (err) {
            console.error("Logout failed", err);
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        fetchTodos(search);
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure?")) return;
        try {
            await api.delete(`/todos/${id}`);
            // Refresh list to keep sync
            fetchTodos(search);
        } catch (err) {
            alert("Failed to delete");
        }
    };

    const handleToggle = async (todo) => {
        try {
            await api.patch(`/todos/${todo.id}`, { is_done: !todo.is_done });
            // Optimistic update
            setTodos(todos.map(t => t.id === todo.id ? { ...t, is_done: !todo.is_done } : t));
        } catch (err) {
            alert("Failed to update");
        }
    };

    if (error) return <div>Error: {error}</div>;

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">
                    {user ? `${user.username}'s Todos` : 'My Todos'}
                </h1>
                <div className="flex gap-2">
                    <button
                        onClick={handleLogout}
                        className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg shadow transition"
                    >
                        Logout
                    </button>
                    <button
                        onClick={() => navigate('/create-tag')}
                        className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg shadow transition"
                    >
                        + Tag
                    </button>
                    <button
                        onClick={() => navigate('/create-todo')}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow transition"
                    >
                        + Todo
                    </button>
                </div>
            </div>

            <form onSubmit={handleSearch} className="mb-6 flex gap-2">
                <div className="relative flex-grow">
                    <input
                        type="text"
                        placeholder="Search todos..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 pl-10"
                    />
                    <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
                </div>
                <button type="submit" className="bg-gray-800 text-white px-6 py-2 rounded-lg hover:bg-gray-700">
                    Search
                </button>
            </form>

            <div className="flex justify-end gap-2 mb-4">
                <button
                    onClick={() => setViewMode('list')}
                    className={`px-4 py-2 rounded-lg transition ${viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                >
                    List View
                </button>
                <button
                    onClick={() => setViewMode('calendar')}
                    className={`px-4 py-2 rounded-lg transition ${viewMode === 'calendar' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                >
                    Calendar View
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-lg overflow-hidden p-4">
                {loading ? (
                    <div className="p-8 text-center text-gray-500">Loading...</div>
                ) : viewMode === 'calendar' ? (
                    <div className="flex justify-center">
                        <Calendar
                            tileContent={({ date, view }) => {
                                if (view === 'month') {
                                    const dayTodos = todos.filter(todo => {
                                        if (!todo.deadline) return false;
                                        const todoDate = new Date(todo.deadline);
                                        return todoDate.getDate() === date.getDate() &&
                                            todoDate.getMonth() === date.getMonth() &&
                                            todoDate.getFullYear() === date.getFullYear();
                                    });

                                    return (
                                        <div className="flex flex-col gap-1 h-full">
                                            {dayTodos.slice(0, 3).map(todo => (
                                                <div key={todo.id} className={`calendar-todo-item ${todo.is_done ? 'done' : ''}`} title={todo.name}>
                                                    {todo.name}
                                                </div>
                                            ))}
                                            {dayTodos.length > 3 && (
                                                <div className="calendar-todo-count">
                                                    +{dayTodos.length - 3} more
                                                </div>
                                            )}
                                        </div>
                                    );
                                }
                            }}
                        />
                    </div>
                ) : todos.length === 0 ? (
                    <div className="p-8 text-center text-gray-500">No todos found.</div>
                ) : (
                    <ul className="divide-y divide-gray-100">
                        {todos.map(todo => (
                            <li key={todo.id} className="p-4 hover:bg-gray-50 transition flex items-center justify-between group">
                                <div className="flex items-center gap-4">
                                    <button
                                        onClick={() => handleToggle(todo)}
                                        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${todo.is_done ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-blue-500'
                                            }`}
                                    >
                                        {todo.is_done && <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>}
                                    </button>
                                    <div>
                                        <p className={`text-lg font-medium transition-all ${todo.is_done ? 'text-gray-400 line-through' : 'text-gray-800'}`}>
                                            {todo.name}
                                        </p>
                                        <div className="flex items-center gap-2 text-sm text-gray-500 mt-1">
                                            {todo.deadline && (
                                                <span className="flex items-center gap-1">
                                                    ⏰ {new Date(todo.deadline).toLocaleString()}
                                                </span>
                                            )}
                                            {todo.tags && todo.tags.length > 0 && (
                                                <div className="flex gap-1">
                                                    {todo.tags.map(tag => (
                                                        <span key={tag.id} className="bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full text-xs">
                                                            #{tag.name}
                                                        </span>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button
                                        onClick={() => navigate(`/edit-todo/${todo.id}`)}
                                        className="text-blue-400 hover:text-blue-600 p-2"
                                        title="Edit"
                                    >
                                        ✏️
                                    </button>
                                    <button
                                        onClick={() => handleDelete(todo.id)}
                                        className="text-red-400 hover:text-red-600 p-2"
                                        title="Delete"
                                    >
                                        🗑️
                                    </button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default TodoList;
