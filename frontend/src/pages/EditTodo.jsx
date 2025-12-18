import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { useNavigate, useParams } from 'react-router-dom';

const EditTodo = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [deadline, setDeadline] = useState('');
    const [tags, setTags] = useState([]);
    const [selectedTags, setSelectedTags] = useState([]);
    const [initialTags, setInitialTags] = useState([]); // Track original tags to calculate diff
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [todoRes, tagsRes] = await Promise.all([
                    api.get(`/todos/${id}`),
                    api.get('/tags')
                ]);

                const todo = todoRes.data;
                setName(todo.name);
                // Format deadline for datetime-local input (YYYY-MM-DDTHH:mm)
                if (todo.deadline) {
                    const date = new Date(todo.deadline);
                    // Adjust to local timezone string manually or use library. 
                    // Simple hack for local ISO-like string:
                    date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
                    setDeadline(date.toISOString().slice(0, 16));
                }

                const currentTagIds = todo.tags.map(t => t.id);
                setSelectedTags(currentTagIds);
                setInitialTags(currentTagIds);

                setTags(tagsRes.data);
            } catch (err) {
                console.error(err);
                setError("Failed to fetch data");
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);

    const handleTagChange = (tagId) => {
        if (selectedTags.includes(tagId)) {
            setSelectedTags(selectedTags.filter(hid => hid !== tagId));
        } else {
            setSelectedTags([...selectedTags, tagId]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            // 1. Update details
            await api.patch(`/todos/${id}`, {
                name,
                deadline: deadline || null
            });

            // 2. Update Tags (Diffing)
            // Tags to add: present in selected but not in initial
            const tagsToAdd = selectedTags.filter(tid => !initialTags.includes(tid));
            // Tags to remove: present in initial but not in selected
            const tagsToRemove = initialTags.filter(tid => !selectedTags.includes(tid));

            await Promise.all([
                ...tagsToAdd.map(tid => api.post(`/todos/${id}/tag/${tid}`)),
                ...tagsToRemove.map(tid => api.delete(`/todos/${id}/tag/${tid}`))
            ]);

            navigate('/todos');
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.message || 'Failed to update todo');
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="container mx-auto p-4 max-w-md">
            <h1 className="text-2xl font-bold mb-4 text-gray-800">Edit Todo</h1>
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
                        Save Changes
                    </button>
                </div>
            </form>
        </div>
    );
};

export default EditTodo;
