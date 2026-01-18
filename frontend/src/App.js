import React, { useState } from 'react';
import './App.css';
import UploadForm from './components/UploadForm';
import ResultsTable from './components/ResultsTable';

function App() {
  const [screeningResult, setScreeningResult] = useState(null);

  const handleResultReceived = (result) => {
    console.log('Received results:', result);
    setScreeningResult(result);
    // Scroll to results
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }, 100);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI Resume Screening System</h1>
        <p className="subtitle">Intelligent candidate evaluation powered by machine learning</p>
      </header>

      <main className="App-main">
        <UploadForm onResultReceived={handleResultReceived} />
        {screeningResult && <ResultsTable batchResults={screeningResult} />}
      </main>

      <footer className="App-footer">
        <p>© 2026 Resume Screening System | University of Bolton / Greater Manchester</p>
      </footer>
    </div>
  );
}

export default App;
