import { useLocation } from 'react-router-dom';

function ResultPage() {
  const { state } = useLocation();

  return (
    <div>
      <h2>Result:</h2>
      <p>{JSON.stringify(state)}</p>
    </div>
  );
}

export default ResultPage;
