import { useEffect } from 'react';
import { X, Clock } from 'lucide-react';

export default function SettingsModal({ setShowSettings, settings, setSettings }) {
    // Close modal on escape key
    useEffect(() => {
        const handleEsc = (e) => { if (e.key === 'Escape') setShowSettings(false); };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setSettings(prev => ({ ...prev, [name]: parseInt(value) || 0 }));
    };

    return (
        <div className="modal-overlay" onClick={() => setShowSettings(false)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <div className="modal-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Clock size={20} /> TIMER SETTINGS
                    </div>
                    <button className="modal-close" onClick={() => setShowSettings(false)}><X size={24} /></button>
                </div>

                <div style={{ fontWeight: 'bold', marginBottom: '1rem', color: '#555' }}>Time (minutes)</div>

                <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                    <div className="input-group">
                        <label style={{ color: '#999', fontSize: '0.8rem' }}>Pomodoro</label>
                        <input
                            type="number"
                            name="pomodoro"
                            value={settings.pomodoro}
                            onChange={handleChange}
                            min="1"
                        />
                    </div>
                    <div className="input-group">
                        <label style={{ color: '#999', fontSize: '0.8rem' }}>Short Break</label>
                        <input
                            type="number"
                            name="shortBreak"
                            value={settings.shortBreak}
                            onChange={handleChange}
                            min="1"
                        />
                    </div>
                    <div className="input-group">
                        <label style={{ color: '#999', fontSize: '0.8rem' }}>Long Break</label>
                        <input
                            type="number"
                            name="longBreak"
                            value={settings.longBreak}
                            onChange={handleChange}
                            min="1"
                        />
                    </div>
                </div>

                <div style={{ background: '#efefef', margin: '-1.5rem', padding: '1.5rem', borderRadius: '0 0 8px 8px', display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
                    <button
                        style={{ background: '#222', color: 'white', fontWeight: 'bold', padding: '0.75rem 2rem' }}
                        onClick={() => setShowSettings(false)}
                    >
                        OK
                    </button>
                </div>

            </div>
        </div>
    );
}
