import React, { useEffect, useState } from 'react';

const MusinsaPage = () => {
  const [data, setData] = useState(null);  // 크롤링 데이터를 저장할 state

  useEffect(() => {
    // 백엔드에서 크롤링한 데이터를 가져오는 함수
    const fetchData = async () => {
      try {
        const response = await fetch('http://your-django-backend-url/api/crawling/musinsa');
        const data = await response.json();
        setData(data);  // 크롤링 데이터를 state에 저장
      } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>무신사 페이지</h2>
      {/* 크롤링 데이터를 화면에 표시 */}
      {data ? (
        <div>
          {/* 데이터 형식에 따라 적절하게 수정하세요 */}
          {data.map((item, index) => (
            <div key={index}>
              <h3>{item['Product_Name']}</h3>
              <p>{item['Price']}</p>
              <a href={item['Product_Link']}>상품 링크</a>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default MusinsaPage;