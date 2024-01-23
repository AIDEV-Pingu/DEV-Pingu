import React, { useEffect, useState } from 'react';
import axios from 'axios';

function MusinsaPage() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('/crawling_results_view?site=musinsa&product_name=your_product_name')
            .then(response => {
                setData(response.data.musinsa);
            });
    }, []);

    return (
        <div>
            <h2>무신사페이지</h2>
            {data.length > 0 ? data.map((item, index) => (
                <div key={index}>
                    <h2>{item.Product_Name}</h2>
                    <p>{item.Price}</p>
                    <a href={item.Product_Link}>Link</a>
                </div>
            )) : <h2>검색된 결과가 없습니다</h2>}
            <br/><br/>
        </div>
    );
}

export default MusinsaPage;
