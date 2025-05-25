import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function UploadPage() {
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append('image', image);

    const response = await axios.post('https://sp-2-nusn.onrender.com/analyze', formData);
    navigate('/result', { state: response.data });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <button type="submit">Analyze</button>
    </form>
  );
}

export default UploadPage;
