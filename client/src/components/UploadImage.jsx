import React, { useState } from 'react';
import './UploadImage.scss';
import { uploadImage } from '../api/api'; // Import the uploadImage function

function UploadImage() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleDragEnter = (event) => {
    event.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setFile(event.dataTransfer.files[0]);
    setDragging(false);
  };

  const handleUpload = async () => {
    try {
      if (!file) return; // No file selected
      const uploadedImage = await uploadImage(file);
      console.log('Image uploaded successfully:', uploadedImage);
      // Add any additional logic here (e.g., display a success message)
    } catch (error) {
      // Handle error (e.g., display error message to user)
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div
      className={`upload-container ${dragging ? 'dragging' : ''}`}
      onDragEnter={handleDragEnter}
      onDragOver={(e) => e.preventDefault()}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <h2>Upload Your Business Idea Sketch</h2>
      <div className="dashed-border"></div>
      <div className="upload-input-container">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="file-input"
        />
        <label htmlFor="file-upload" className="file-label">
          {file ? file.name : 'Choose an image or drag it here'}
        </label>
      </div>
      <button onClick={handleUpload} disabled={!file}>
        Upload
      </button>
    </div>
  );
}

export default UploadImage;
