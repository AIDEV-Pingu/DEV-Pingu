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

class UploadPage extends React.Component {
  state = {
    selectedImage: null,
    image: null,
    ocrImage: null,
    ocrResult: null,
    ocrChecked: false,  // OCR 결과를 확인했는지 여부를 나타내는 상태변수 추가
    loading: false,
  };
  
  handleHomeClick = () => {
    this.setState({
      selectedImage: null,
      image: null,
      ocrImage: null,
      ocrResult: null,
      ocrChecked: false,  // 홈 버튼을 누르면 OCR 결과 확인 여부도 초기화
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
      loading: true,
      image: URL.createObjectURL(file),
    });

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
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
      
      if (data.ocrResult) {
        this.setState({
          ocrResult: data.ocrResult
        });
      }
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    } finally {
      this.setState({
        loading: false,  // 로딩 종료
        ocrChecked: true,  // OCR 결과 확인 완료
      });
    }
  };

  render() {
    return (
      <div>
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

        <div id="ocr-result">
          {this.state.ocrChecked && !this.state.ocrResult ? 'OCR 결과가 없습니다.' : this.state.ocrResult}
        </div>

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
      </div>
    );
  }
}

export default UploadPage;