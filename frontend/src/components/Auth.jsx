import { useState, useEffect } from 'react';
import axios from 'axios';
import { X } from 'lucide-react';

export default function Auth({ setShowAuth, setUser }) {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');

    // Close modal on escape key
    useEffect(() => {
        const handleEsc = (e) => { if (e.key === 'Escape') setShowAuth(false); };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            if (isLogin) {
                const res = await axios.post('http://127.0.0.1:8000/api/login', { username, password });
                setUser({ username: res.data.username });
                setShowAuth(false);
            } else {
                await axios.post('http://127.0.0.1:8000/api/signup', { username, email, password });
                setIsLogin(true); // switch to login after successful signup
                setError('Signup successful. Please login.');
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred');
        }
    };

    return (
        <div className="modal-overlay" onClick={() => setShowAuth(false)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <div className="modal-title">{isLogin ? 'LOG IN' : 'CREATE ACCOUNT'}</div>
                    <button className="modal-close" onClick={() => setShowAuth(false)}><X size={24} /></button>
                </div>

                {error && <div style={{ color: 'red', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}

                <form onSubmit={handleSubmit}>
                    {(!isLogin) && (
                        <div className="input-group">
                            <label>EMAIL</label>
                            <input
                                type="email"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                required
                            />
                        </div>
                    )}
                    <div className="input-group">
                        <label>USERNAME</label>
                        <input
                            type="text"
                            value={username}
                            onChange={e => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label>PASSWORD</label>
                        <input
                            type="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" className="modal-submit">
                        {isLogin ? 'Log In' : 'Sign Up'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem' }}>
                    {isLogin ? "Don't have an account? " : "Already have an account? "}
                    <span
                        style={{ fontWeight: 'bold', textDecoration: 'underline', cursor: 'pointer' }}
                        onClick={() => { setIsLogin(!isLogin); setError(''); }}
                    >
                        {isLogin ? 'Create Account' : 'Log In'}
                    </span>
                </div>
            </div>
        </div>
    );
}
