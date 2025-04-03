import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [images, setImages] = useState({});

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setImages(response.data);
    } catch (error) {
      console.error("Error uploading file", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Fabric Inspection Dashboard</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      {images.original_image && (
        <div>
          <h2>Results</h2>
          <img src={`http://127.0.0.1:8000/${images.original_image}`} alt="Original" width="300px" />
          <p>Original Image</p>

          <img src={`http://127.0.0.1:8000/${images.grayscale_image}`} alt="Grayscale" width="300px" />
          <p>Grayscale with Defects</p>

          <img src={`http://127.0.0.1:8000/${images.corrected_image}`} alt="Corrected" width="300px" />
          <p>Corrected Image (RGB for AR)</p>
        </div>
      )}
    </div>
  );
}

export default App;