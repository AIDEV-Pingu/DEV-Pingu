import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import UploadPage from './UploadPage';
{/*}
import NaverPage from './NaverPage';
import SsgPage from './SsgPage';
import CoupangPage from './CoupangPage';
import MusinsaPage from './MusinsaPage';
import naver from './버튼 이미지/naver.png';
import ssg from './버튼 이미지/ssg.png';
import loading from './버튼 이미지/mintloading.gif';
import musinsa from './버튼 이미지/musinsa.png';
import pinguw from './버튼 이미지/pinguw.png';
*/}

class MainPage extends React.Component {

  state = {
    isUploadPage: false, // 새로운 state 추가
  };

  handleClick = () => {
    this.setState({
      isUploadPage: true, // UploadPage로 이동할 때 state 업데이트
    });
  };

  render() {
    return (
      <div>

        <div className="button-container" style={{ marginTop: '20px' }}>
          {!this.state.isUploadPage && ( // isUploadPage가 false일 때만 버튼 렌더링
            <Link to="/upload" onClick={this.handleClick}> {/* 클릭 이벤트 추가 */}
              <button type="button">
                Upload Image
              </button>
            </Link>
          )}
        </div>

        <Routes>
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </div>
    );
  }
}

export default MainPage;