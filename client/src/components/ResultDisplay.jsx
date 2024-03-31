import React from 'react';

function ResultDisplay() {
  // Example data for displaying result
  const resultData = {
    insight1: 'Generated insight 1',
    insight2: 'Generated insight 2',
    insight3: 'Generated insight 3',
  };

  return (
    <div className="result-container">
      <h2>Generated Insights</h2>
      <ul>
        {Object.entries(resultData).map(([key, value]) => (
          <li key={key}>{value}</li>
        ))}
      </ul>
    </div>
  );
}

export default ResultDisplay;
