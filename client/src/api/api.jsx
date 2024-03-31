// api/api.jsx
import { getStorage, ref, uploadBytes } from "firebase/storage";

// Initialize Firebase Storage
const storage = getStorage();

export const uploadImage = async (imageFile) => {
  try {
    // Create a reference to the storage location
    const storageRef = ref(storage, `images/${imageFile.name}`);

    // Upload the image file to Firebase Storage
    const snapshot = await uploadBytes(storageRef, imageFile);

    // Get the download URL for the uploaded image
    const downloadURL = await snapshot.ref.getDownloadURL();

    // Return the download URL
    return downloadURL;
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};
