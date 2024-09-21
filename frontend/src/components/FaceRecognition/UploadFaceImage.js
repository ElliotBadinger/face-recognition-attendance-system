// Component for uploading face images
import React, { useState } from 'react';

const UploadFaceImage = () => {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageChange = (event) => {
    setSelectedImage(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission, send image data to backend
    console.log(selectedImage);
    // Reset form after submission
    setSelectedImage(null);
  };

  return (
    <div>
      <h2>Upload Face Image</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="image">Select Image:</label>
          <input
            type="file"
            id="image"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default UploadFaceImage;
