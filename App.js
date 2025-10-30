// webapp/src/App.js
import React, { useEffect, useState } from 'react';

function App() {
  const [scores, setScores] = useState([]);
  useEffect(() => {
    const fetch = async () => {
      const res = await fetch('http://localhost:8000/latest_scores?limit=50');
      const data = await res.json();
      setScores(data);
    };
    fetch();
    const id = setInterval(fetch, 2000); // poll every 2s
    return () => clearInterval(id);
  }, []);
  return (
    <div style={{padding:20}}>
      <h2>Fraud Scores (latest)</h2>
      <table border="1" cellPadding="6">
        <thead><tr><th>tx_id</th><th>time</th><th>score</th><th>label</th></tr></thead>
        <tbody>
          {scores.map(s => (
            <tr key={s.tx_id}>
              <td>{s.tx_id}</td>
              <td>{new Date(s.time*1000).toLocaleString()}</td>
              <td>{s.score.toFixed(4)}</td>
              <td>{s.label}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
