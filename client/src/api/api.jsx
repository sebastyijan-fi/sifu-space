// api/api.jsx

const BASE_URL = 'http://127.0.0.1:5001';

export const uploadImage = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload image');
    }

    const contentType = response.headers.get('content-type');
    if (contentType && contentType.indexOf('application/json') !== -1) {
      return await response.json(); // Return JSON data
    } else {
      return await response.text(); // Return plain text
    }
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};
