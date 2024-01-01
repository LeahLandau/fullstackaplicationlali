import React, { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api') // Assuming your Flask API endpoint is `/api`
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Frontend</h1>
        <p>Message from Flask API:</p>
        <p>{message}</p>
      </header>
    </div>
  );
}

export default App;
