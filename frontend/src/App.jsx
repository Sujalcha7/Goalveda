import { useState, useEffect } from 'react';
import { Settings, UserCircle2, CheckCircle2 } from 'lucide-react';
import Timer from './components/Timer';
import TaskList from './components/TaskList';
import Auth from './components/Auth';
import SettingsModal from './components/SettingsModal';
import './App.css';
import axios from 'axios';

function App() {
  const [theme, setTheme] = useState('pomodoro'); // pomodoro, short-break, long-break
  const [showAuth, setShowAuth] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [user, setUser] = useState(null);

  // Settings
  const [settings, setSettings] = useState({
    pomodoro: 25,
    shortBreak: 5,
    longBreak: 15,
  });

  useEffect(() => {
    // Update body class for theme
    document.body.className = `theme-${theme}`;
  }, [theme]);

  // Handle Logout
  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div>
      <header className="header">
        <div className="logo">
          <CheckCircle2 color="white" size={24} />
          Goalveda
        </div>
        <div className="header-buttons">
          <button onClick={() => setShowSettings(true)}>
            <Settings size={18} /> Settings
          </button>
          {!user ? (
            <button onClick={() => setShowAuth(true)}>
              <UserCircle2 size={18} /> Login
            </button>
          ) : (
            <button onClick={handleLogout}>
              <UserCircle2 size={18} /> Logout
            </button>
          )}
        </div>
      </header>

      <Timer
        theme={theme}
        setTheme={setTheme}
        settings={settings}
        user={user}
      />

      <TaskList user={user} theme={theme} setShowAuth={setShowAuth} />

      {showAuth && <Auth setShowAuth={setShowAuth} setUser={setUser} />}
      {showSettings && <SettingsModal setShowSettings={setShowSettings} settings={settings} setSettings={setSettings} />}
    </div>
  );
}

export default App;
