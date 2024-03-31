import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import Header from './components/Header';
import UploadImage from './components/UploadImage';
import ResultDisplay from './components/ResultDisplay';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <Routes> {/* Use Routes instead of Switch */}
            {/* Route for uploading image */}
            <Route path="/" element={<UploadImage />} />
            {/* Route for displaying results */}
            <Route path="/results" element={<ResultDisplay />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
