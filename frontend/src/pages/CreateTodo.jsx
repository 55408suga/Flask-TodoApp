import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

const CreateTodo = () => {
    const [name, setName] = useState('');
    const [deadline, setDeadline] = useState('');
    const [tags, setTags] = useState([]);
    const [selectedTags, setSelectedTags] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTags = async () => {
            try {
                const response = await api.get('/tags');
                setTags(response.data);
            } catch (err) {
                console.error("Failed to fetch tags", err);
            }
        };
        fetchTags();
    }, []);

    const handleTagChange = (tagId) => {
        if (selectedTags.includes(tagId)) {
            setSelectedTags(selectedTags.filter(id => id !== tagId));
        } else {
            setSelectedTags([...selectedTags, tagId]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            // 1. Create Todo
            const response = await api.post('/todos', {
                name,
                deadline: deadline || null
            });

            const newTodo = response.data;
            if (!newTodo || !newTodo.id) {
                throw new Error("Failed to retrieve created todo ID");
            }

            // 2. Link Tags
            if (selectedTags.length > 0) {
                await Promise.all(selectedTags.map(tagId =>
                    api.post(`/todos/${newTodo.id}/tag/${tagId}`)
                ));
            }

            navigate('/todos');
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.message || 'Failed to create todo');
        }
    };

    return (
        <div className="container mx-auto p-4 max-w-md">
            <h1 className="text-2xl font-bold mb-4 text-gray-800">Create New Todo</h1>
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Task Name
                    </label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500 transition"
                        placeholder="Enter task name"
                        required
                    />
                </div>

                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Deadline
                    </label>
                    <input
                        type="datetime-local"
                        value={deadline}
                        onChange={(e) => setDeadline(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500 transition"
                    />
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Tags
                    </label>
                    <div className="flex flex-wrap gap-2 text-gray-700">
                        {tags.length === 0 && <p className="text-gray-400 text-sm">No tags available.</p>}
                        {tags.map(tag => (
                            <label key={tag.id} className={`cursor-pointer px-3 py-1 rounded-full border text-sm transition select-none ${selectedTags.includes(tag.id)
                                    ? 'bg-purple-100 border-purple-400 text-purple-700'
                                    : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                                }`}>
                                <input
                                    type="checkbox"
                                    className="hidden"
                                    checked={selectedTags.includes(tag.id)}
                                    onChange={() => handleTagChange(tag.id)}
                                />
                                #{tag.name}
                            </label>
                        ))}
                    </div>
                </div>

                {error && <p className="text-red-500 text-sm mb-4 bg-red-50 p-2 rounded">{error}</p>}

                <div className="flex items-center justify-between mt-6">
                    <button
                        type="button"
                        onClick={() => navigate('/todos')}
                        className="bg-gray-100 text-gray-600 hover:bg-gray-200 font-medium py-2 px-4 rounded transition"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded shadow transition"
                    >
                        Create Task
                    </button>
                </div>
            </form>
        </div>
    );
};

export default CreateTodo;
