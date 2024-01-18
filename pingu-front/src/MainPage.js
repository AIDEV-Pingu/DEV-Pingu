import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import NaverPage from './NaverPage';
import SsgPage from './SsgPage';
import CoupangPage from './CoupangPage';
import MusinsaPage from './MusinsaPage';
import naver from './버튼 이미지/naver.png';
import ssg from './버튼 이미지/ssg.png';
import loading from './버튼 이미지/mintloading.gif';
import musinsa from './버튼 이미지/musinsa.png';
import pinguw from './버튼 이미지/pinguw.png';

class MainPage extends React.Component {
  state = {
    selectedImage: null,
    image: null,
    ocrImage: null,
    loading: false,
  };

  handleHomeClick = () => {
    this.setState({
      selectedImage: null,
      image: null,
      ocrImage: null,
      loading: false,
    });
  };

  handleImageChange = (e) => {
    const file = e.target.files[0];
    this.setState({
      selectedImage: file
    });
  };

  handleUploadClick = async () => {
    const file = this.state.selectedImage;
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    this.setState({
      loading: true, // 로딩 시작
      image: URL.createObjectURL(file), // 원본 이미지 미리보기 설정
    });

    try {
      const response = await fetch('http://your-backend-url/api/ocr', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      if (data.ocrImage) {
        this.setState({
          ocrImage: data.ocrImage
        });
      }
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    } finally {
      this.setState({
        loading: false, // 로딩 종료
      });
    }
  };

  render() {
    return (
      <div>
        <header style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start', backgroundImage: 'linear-gradient(to right, #E91E63, #9C27B0, #667eea)', marginBottom: '20px' }}>
          <Link to="/" onClick={this.handleHomeClick}>
            <button type="button" style={{ border: 'none', background: 'none' }}>
              <img src={pinguw} className="button-img" style={{ width: '100px', height: '100px' }} alt="Home" />
              <h2 style={{ color: '#FFFFFF' }}>Pingu OCR</h2>
            </button>
          </Link>
        </header>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <input type="file" id="upload" onChange={this.handleImageChange} />
          <button id="upload-button" onClick={this.handleUploadClick}>Upload</button>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
          {this.state.loading ? (
            <img src={loading} alt="Loading..." />
          ) : (
            this.state.ocrImage ? (
              <img src={this.state.ocrImage} className="uploaded-img" alt="OCR Image" />
            ) : (
              this.state.image && <img src={this.state.image} className="uploaded-img" alt="Uploaded" />
            )
          )}
        </div>


        <div id="ocr-result"></div>

        <div className="button-container" style={{ marginTop: '20px' }}>
          <Link to="/naver_P">
            <button type="button">
              <img src={naver} className="button-img" alt="naver" />
            </button>
          </Link>

          <Link to="/ssg_P">
            <button type="button">
              <img src={ssg} className="button-img" alt="ssg" />
            </button>
          </Link>

          <Link to="/musinsa_P">
            <button type="button">
              <img src={musinsa} className="button-img" alt="musinsa" />
            </button>
          </Link>
        </div>

        <Routes>
          <Route path="/naver_P" element={<NaverPage ocrResult={this.state.ocrResult} />} />
          <Route path="/ssg_P" element={<SsgPage ocrResult={this.state.ocrResult} />} />
          <Route path="/coupang_P" element={<CoupangPage ocrResult={this.state.ocrResult} />} />
          <Route path="/musinsa_P" element={<MusinsaPage ocrResult={this.state.ocrResult} />} />
        </Routes>
      </div>
    );
  }
}

export default MainPage;