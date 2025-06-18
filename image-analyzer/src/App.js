// App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Optional: Make sure this file exists or comment it out

function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false); // 👈 Loading state

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!image) {
      setResult('Please upload an image first');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    setLoading(true); // 👈 Start loading

    try {
      const res = await axios.post('https://sp-ign5.onrender.com/analyze', formData);
      setResult(`Predicted Class: ${res.data.predicted_class}`);
    } catch (err) {
      console.error(err);
      setResult('Error analyzing image');
    } finally {
      setLoading(false); // 👈 Stop loading
    }
  };

  return (
    <div className="App" style={{ padding: 20 }}>
      <h2>Banana Leaf Nutrient Analyzer</h2>
      <input type="file" onChange={handleImageChange} />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
      <p><strong>Result:</strong> {loading ? 'Loading...' : result}</p>
    </div>
  );
}

export default App;
