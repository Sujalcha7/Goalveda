import { useState, useEffect } from 'react';
import axios from 'axios';
import { PlusCircle, MoreVertical, Check } from 'lucide-react';

export default function TaskList({ user, theme, setShowAuth }) {
    const [tasks, setTasks] = useState([]);
    const [showAdd, setShowAdd] = useState(false);
    const [newTaskName, setNewTaskName] = useState('');
    const [estPomodoros, setEstPomodoros] = useState(1);
    const [toastMsg, setToastMsg] = useState('');

    const fetchTasks = async () => {
        if (!user) { setTasks([]); return; }
        try {
            const res = await axios.get(`http://127.0.0.1:8000/api/tasks/${user.username}`);
            setTasks(res.data);
        } catch (err) { }
    };

    useEffect(() => {
        fetchTasks();
    }, [user]);

    const showToast = (msg) => {
        setToastMsg(msg);
        setTimeout(() => setToastMsg(''), 3000);
    };

    const handleAddTask = async () => {
        if (!user) {
            setShowAuth(true);
            return;
        }
        if (!newTaskName.trim()) return;

        try {
            await axios.post('http://127.0.0.1:8000/api/tasks', {
                username: user.username,
                task_name: newTaskName,
                est_gol: estPomodoros
            });
            showToast('Task added successfully');
            setNewTaskName('');
            setEstPomodoros(1);
            setShowAdd(false);
            fetchTasks();
        } catch (err) { alert('Failed to add task'); }
    };

    const deleteBtn = async (task_name) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/api/tasks/${user.username}/${encodeURIComponent(task_name)}`);
            fetchTasks();
        } catch (err) { }
    };

    // The active task highlight color based on theme
    const activeBorderColor = theme === 'pomodoro' ? 'var(--bg-pomodoro)' : theme === 'short-break' ? 'var(--bg-short-break)' : 'var(--bg-long-break)';

    return (
        <div style={{ maxWidth: '480px', margin: '0 auto' }}>
            <div className="tasks-header">
                <div className="tasks-title">Tasks</div>
                <button style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '0.4rem' }}>
                    <MoreVertical size={18} />
                </button>
            </div>

            {tasks.map(task => {
                const isDone = task.completed_pomodoros >= task.est_gol;
                return (
                    <div key={task.task_name} className={`task-item`} style={{ borderLeftColor: isDone ? '#ccc' : activeBorderColor }}>
                        <div className="task-left">
                            <div className={`task-check ${isDone ? 'completed' : ''}`}>
                                {isDone && <Check size={16} />}
                            </div>
                            <div className={`task-title ${isDone ? 'completed' : ''}`}>
                                {task.task_name}
                            </div>
                        </div>
                        <div className="task-right">
                            <span>{task.completed_pomodoros} / {task.est_gol}</span>
                            <button
                                onClick={() => deleteBtn(task.task_name)}
                                style={{ backgroundColor: 'transparent', color: '#999', padding: '0.2rem' }}
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                )
            })}

            {!showAdd ? (
                <button className="add-task-btn" onClick={() => setShowAdd(true)}>
                    <PlusCircle size={20} /> Add Task
                </button>
            ) : (
                <div style={{ background: 'white', padding: '1rem', borderRadius: '8px', color: '#333', marginTop: '1rem' }}>
                    <input
                        type="text"
                        placeholder="What are you working on?"
                        style={{ width: '100%', fontSize: '1.1rem', border: 'none', outline: 'none', fontWeight: 'bold', marginBottom: '1rem' }}
                        value={newTaskName}
                        onChange={(e) => setNewTaskName(e.target.value)}
                        autoFocus
                    />
                    <div style={{ fontWeight: 'bold', marginBottom: '0.5rem', color: '#555' }}>Est Pomodoros</div>
                    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
                        <input
                            type="number"
                            min="1"
                            style={{ width: '80px', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc', background: '#eee' }}
                            value={estPomodoros}
                            onChange={(e) => setEstPomodoros(parseInt(e.target.value))}
                        />
                        <button style={{ background: 'white', color: '#555', border: '1px solid #ccc', boxShadow: '0 2px 2px rgba(0,0,0,0.1)' }} onClick={() => setEstPomodoros(prev => prev + 1)}>+</button>
                        <button style={{ background: 'white', color: '#555', border: '1px solid #ccc', boxShadow: '0 2px 2px rgba(0,0,0,0.1)' }} onClick={() => setEstPomodoros(prev => Math.max(1, prev - 1))}>-</button>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', background: '#efefef', margin: '-1rem', padding: '1rem', borderRadius: '0 0 8px 8px', marginTop: '1rem' }}>
                        <button style={{ background: 'transparent', color: '#888', fontWeight: 'bold' }} onClick={() => setShowAdd(false)}>Cancel</button>
                        <button style={{ background: '#222', color: 'white', px: '1.5rem', fontWeight: 'bold' }} onClick={handleAddTask}>Save</button>
                    </div>
                </div>
            )}

            {toastMsg && (
                <div className="toast">{toastMsg}</div>
            )}
        </div>
    );
}
