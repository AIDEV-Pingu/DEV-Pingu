import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NaverPage = ({ ocrResult }) => {
  const [crawlingResult, setCrawlingResult] = useState(null);

  useEffect(() => {
    const getCrawlingResult = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/crawl/naver', {
          text: ocrResult,
        });
        setCrawlingResult(response.data.result);
      } catch (error) {
        console.error(error);
      }
    };

    if (ocrResult) {
      getCrawlingResult();
    }
  }, [ocrResult]);

  return (
    <div>
      <h2>Naver 페이지</h2>
      {crawlingResult && <div>{crawlingResult}</div>}
    </div>
  );
}

export default NaverPage;