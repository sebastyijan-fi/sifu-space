import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import UploadImage from './components/UploadImage';
import ResultDisplay from './components/ResultDisplay';
import Footer from './components/Footer';
import Login from './components/Login'; // Import Login component
import Register from './components/Register'; // Import Register component

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<UploadImage />} />
            <Route path="/results" element={<ResultDisplay />} />
            <Route path="/login" element={<Login />} /> {/* Route to Login component */}
            <Route path="/register" element={<Register />} /> {/* Route to Register component */}
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
