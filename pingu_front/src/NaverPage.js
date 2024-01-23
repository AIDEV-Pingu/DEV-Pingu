import React, { useEffect, useState } from 'react';
import axios from 'axios';

function NaverPage() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('/crawling_results_view?site=naver&product_name=your_product_name')
            .then(response => {
                setData(response.data.naver);
            });
    }, []);

    return (
        <div>
            <h2>네이버페이지</h2>
            {data.length > 0 ? data.map((item, index) => (
                <div key={index}>
                    <h2>{item.title}</h2>
                    <p>{item.lprice}</p>
                    <a href={item.link}>Link</a>
                </div>
            )) : <h2>검색된 결과가 없습니다</h2>}
            <br/><br/>
        </div>
    );
}

export default NaverPage;
