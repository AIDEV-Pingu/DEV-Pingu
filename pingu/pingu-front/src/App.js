// App.js
import React from 'react';
import { BrowserRouter as Router, Link, Routes, Route } from 'react-router-dom';
import MainPage from './MainPage';
import UploadPage from './UploadPage';
import NaverPage from './NaverPage';
import SsgPage from './SsgPage';
import CoupangPage from './CoupangPage';
import MusinsaPage from './MusinsaPage';
import './App.css';
import pinguw from './버튼 이미지/pinguw.png';

class App extends React.Component {
  handleHomeClick = () => {
    this.setState({
      selectedImage: null,
      image: null,
      ocrImage: null,
      loading: false,
    });
  };

  render() {
    return (
      <Router>
        <header style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start', backgroundImage: 'linear-gradient(to right, #E91E63, #9C27B0, #667eea)', marginBottom: '20px' }}>
          <Link to="/" onClick={this.handleHomeClick}>
            <button type="button" style={{ border: 'none', background: 'none' }}>
              <img src={pinguw} className="button-img" style={{ width: '100px', height: '100px' }} alt="Home" />
              <h2 style={{ color: '#FFFFFF' }}>Pingu OCR</h2>
            </button>
          </Link>
        </header>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/naver_P" element={<NaverPage />} />
          <Route path="/ssg_P" element={<SsgPage />} />
          <Route path="/coupang_P" element={<CoupangPage />} />
          <Route path="/musinsa_P" element={<MusinsaPage />} />
        </Routes>
      </Router>
    );
  }
}

export default App;
