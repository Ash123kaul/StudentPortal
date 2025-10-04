// firebase.js
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth"; // Import authentication

const firebaseConfig = {
  apiKey: "AIzaSyBSZ2Q4h5qC6DdofCHVaAGyCKkJBPDK0Gw",
  authDomain: "student-portal-cf3fa.firebaseapp.com",
  databaseURL: "https://student-portal-cf3fa-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "student-portal-cf3fa",
  storageBucket: "student-portal-cf3fa.firebasestorage.app",
  messagingSenderId: "259776751437",
  appId: "1:259776751437:web:211d3c709e22106d463904",
  measurementId: "G-S7B9ZR9EWW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app); // Initialize authentication

export { app, auth, analytics }; // Export for use in other files