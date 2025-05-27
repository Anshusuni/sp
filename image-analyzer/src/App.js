import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Make sure this file exists or remove this line

function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState('');

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

    try {
      const res = await axios.post('https://sp-ign5.onrender.com/analyze', formData);
      setResult(`Predicted Class: ${res.data.predicted_class}`);
    } catch (err) {
      console.error(err);
      setResult('Error analyzing image');
    }
  };

  return (
    <div className="App" style={{ padding: 20 }}>
      <h2>Image Analyzer</h2>
      <input type="file" onChange={handleImageChange} />
      <button onClick={handleAnalyze}>Analyze</button>
      <p><strong>Result:</strong> {result}</p>
    </div>
  );
}

export default App;
