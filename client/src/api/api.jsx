// api/api.jsx
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { storage } from '../firebase';

export const uploadImage = async (imageFile) => {
  try {
    // Retrieve the user's UID from session storage
    const uid = sessionStorage.getItem('uid');

    // Create a reference in Firebase Storage
    const storageRef = ref(storage, `images/${imageFile.name}`);

    // Upload the image file to Firebase Storage
    const snapshot = await uploadBytes(storageRef, imageFile);

    // Get the download URL for the uploaded image
    const downloadURL = await getDownloadURL(snapshot.ref);

    // Send the download URL and the user's UID to your Flask backend
    const response = await fetch('http://127.0.0.1:5001/upload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ imageUrl: downloadURL, uid: uid }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Optionally process the response from the backend
    const responseData = await response.json();

    // Return both the download URL and the backend's response
    return { downloadURL, responseData };
  } catch (error) {
    console.error('Error uploading image and sending URL to backend:', error);
    throw error;
  }
};
