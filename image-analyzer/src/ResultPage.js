import React from 'react';
import { useLocation } from 'react-router-dom';

function ResultPage() {
  const { state } = useLocation();

  return (
    <div>
      <h2>Analysis Result:</h2>
      {state ? (
        <pre>{JSON.stringify(state, null, 2)}</pre>
      ) : (
        <p>No result available.</p>
      )}
    </div>
  );
}

export default ResultPage;
