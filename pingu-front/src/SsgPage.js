import React, { useEffect, useState } from 'react';
import axios from 'axios';

function SsgPage() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('/crawling_results_view?site=ssg&product_name=your_product_name')
            .then(response => {
                setData(response.data.ssg);
            });
    }, []);

    return (
        <div>
            <h2>SSG페이지</h2>
            {data.length > 0 ? data.map((item, index) => (
                <div key={index}>
                    <h2>{item.product_names}</h2>
                    <p>{item.prices}</p>
                    <a href={item.product_urls}>Link</a>
                </div>
            )) : <h2>검색된 결과가 없습니다</h2>}
            <br/><br/>
        </div>
    );
}

export default SsgPage;
