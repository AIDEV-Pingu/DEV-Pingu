import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import NaverPage from './NaverPage';
import SsgPage from './SsgPage';
import CoupangPage from './CoupangPage';
import MusinsaPage from './MusinsaPage';
import naver from './버튼 이미지/naver.png';
import ssg from './버튼 이미지/ssg.png';
import coupang from './버튼 이미지/coupang.png';
import musinsa from './버튼 이미지/musinsa.png';
import pinguw from './버튼 이미지/pinguw.png';

class MainPage extends React.Component {
  state = {
    image: null,
  };

  handleHomeClick = () => {
    this.setState({
      image: null,
    });
  };

  handleImageChange = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('image', file);
    
    // 업로드한 이미지를 먼저 화면에 표시
    this.setState({
      image: URL.createObjectURL(file)
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
        
      // 백엔드에서 OCR 처리된 이미지의 URL을 'ocrImage' 필드에 담아서 보내준다고 가정
      if (data.ocrImage) {  // OCR 처리된 이미지가 있을 때만 상태를 업데이트
        this.setState({
          ocrImage: data.ocrImage  // OCR 처리된 이미지의 URL을 상태에 저장
        });
      }
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
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
            <button id="upload-button">Upload</button>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
            {this.state.image && <img src={this.state.image} className="uploaded-img" alt="Uploaded" />}
            {this.state.ocrImage && <img src={this.state.ocrImage} className="uploaded-img" alt="OCR Image" />}
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

          <Link to="/coupang_P">
            <button type="button">
              <img src={coupang} className="button-img" alt="coupang" />
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