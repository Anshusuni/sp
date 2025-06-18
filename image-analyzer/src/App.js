// App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Optional: Make sure this file exists or comment it out
const [imagePreview, setImagePreview] = useState(null);

function App() {
  const [image, setImage] = useState(null);
   const [imagePreview, setImagePreview] = useState(null);
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
    <input type="file" accept="image/*" onChange={handleImageChange} />

    {imagePreview && (
      <div style={{ marginTop: 20 }}>
        <p><strong>Preview:</strong></p>
        <img src={imagePreview} alt="Uploaded preview" style={{ maxWidth: '300px', height: 'auto' }} />
      </div>
    )}

    <button onClick={handleAnalyze} disabled={loading}>
      {loading ? 'Analyzing...' : 'Analyze'}
    </button>

    <p><strong>Result:</strong> {loading ? 'Loading...' : result}</p>
  </div>
);

useEffect(() => {
  return () => {
    if (imagePreview) URL.revokeObjectURL(imagePreview);
  };
}, [imagePreview]);

}

export default App;
