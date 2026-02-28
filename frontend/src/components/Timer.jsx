import { useState, useEffect, useRef } from 'react';

export default function Timer({ theme, setTheme, settings, user }) {
    const [timeLeft, setTimeLeft] = useState(settings.pomodoro * 60);
    const [isRunning, setIsRunning] = useState(false);

    // Update time when settings/theme changes (only if not running)
    useEffect(() => {
        if (!isRunning) {
            if (theme === 'pomodoro') setTimeLeft(settings.pomodoro * 60);
            if (theme === 'short-break') setTimeLeft(settings.shortBreak * 60);
            if (theme === 'long-break') setTimeLeft(settings.longBreak * 60);
        }
    }, [theme, settings]);

    useEffect(() => {
        let interval = null;
        if (isRunning && timeLeft > 0) {
            interval = setInterval(() => setTimeLeft(prev => prev - 1), 1000);
        } else if (timeLeft === 0 && isRunning) {
            setIsRunning(false);
            clearInterval(interval);
            playAlarm();
            // Auto switch or just notify (Pomofocus stops and plays alarm)
        }
        return () => clearInterval(interval);
    }, [isRunning, timeLeft]);

    // Audio for finish
    const playAlarm = () => {
        // We would use an audio file here. For now we use the browser's native AudioContext as a beep.
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            oscillator.type = 'sine';
            oscillator.frequency.value = 800;

            gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
            gainNode.gain.linearRampToValueAtTime(1, audioCtx.currentTime + 0.01);
            gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.5);

            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.5);
        } catch (e) { console.error('Audio play failed', e) }
    };

    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;

    // Format MM:SS
    const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    // Set tab title
    useEffect(() => {
        document.title = `${formattedTime} - Time to focus!`;
    }, [formattedTime]);

    // Dynamic button color
    const btnColor = theme === 'pomodoro' ? 'var(--bg-pomodoro)' : theme === 'short-break' ? 'var(--bg-short-break)' : 'var(--bg-long-break)';

    return (
        <div className="timer-container">
            <div className="timer-modes">
                <button
                    className={`mode-btn ${theme === 'pomodoro' ? 'active' : ''}`}
                    onClick={() => { setTheme('pomodoro'); setIsRunning(false); }}
                >
                    Pomodoro
                </button>
                <button
                    className={`mode-btn ${theme === 'short-break' ? 'active' : ''}`}
                    onClick={() => { setTheme('short-break'); setIsRunning(false); }}
                >
                    Short Break
                </button>
                <button
                    className={`mode-btn ${theme === 'long-break' ? 'active' : ''}`}
                    onClick={() => { setTheme('long-break'); setIsRunning(false); }}
                >
                    Long Break
                </button>
            </div>

            <div className="time-display">
                {formattedTime}
            </div>

            <button
                className={`start-btn ${isRunning ? 'pressed' : ''}`}
                style={{ color: btnColor }}
                onClick={() => setIsRunning(!isRunning)}
            >
                {isRunning ? 'PAUSE' : 'START'}
            </button>
        </div>
    );
}
