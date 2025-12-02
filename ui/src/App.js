import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/run-agent', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.text();
      setOutput(result);
      setError('');
    } catch (error) {
      setError('Error running the agent: ' + error.message);
      setOutput('');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Digital Agent UI</h1>
        <div className="card">
          <input type="file" onChange={handleFileChange} accept=".tsv" />
          <button onClick={handleSubmit}>Run Agent</button>
          {error && <p className="error">{error}</p>}
        </div>
        {output && (
          <div className="output">
            <h2>Agent Output</h2>
            <pre>{output}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
