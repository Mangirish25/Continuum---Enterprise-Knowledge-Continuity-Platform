import { useState, useEffect } from 'react';

export default function App() {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
  const [apiStatus, setApiStatus] = useState<'checking' | 'reachable' | 'unreachable'>('checking');

  useEffect(() => {
    fetch(`${apiBaseUrl.replace(/\/$/, '')}/health`)
      .then((res) => (res.ok ? setApiStatus('reachable') : setApiStatus('unreachable')))
      .catch(() => setApiStatus('unreachable'));
  }, [apiBaseUrl]);

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>EKCP — Enterprise Knowledge Continuity Platform</h1>
      <p style={{ color: '#666' }}>Web Frontend Scaffolding Placeholder Page (Task 002)</p>
      
      <div style={{ background: '#f5f5f5', padding: '1rem', borderRadius: '8px', marginTop: '1.5rem' }}>
        <h3>Build & Configuration Verification</h3>
        <ul>
          <li><strong>Configured API Base URL:</strong> <code>{apiBaseUrl}</code></li>
          <li><strong>API Health Status:</strong> <span>{apiStatus}</span></li>
          <li><strong>Environment:</strong> <code>{import.meta.env.MODE}</code></li>
        </ul>
      </div>
    </div>
  );
}
