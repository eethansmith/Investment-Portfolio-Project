import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

function StockGraph({ ticker }) { // Use destructuring to get the ticker prop
    const [stockData, setStockData] = useState([]);

    useEffect(() => {
        // Ensure the ticker value is included in the fetch URL
        fetch(`http://localhost:8000/api/graph_stock/${ticker}/`)
            .then(response => response.json())
            .then(data => setStockData(data))
            .catch(error => console.error('Error fetching data:', error));
    }, [ticker]); // Include ticker in the dependency array

    const chartData = {
        labels: stockData.map(data => data.date),
        datasets: [{
            label: `${ticker} Stock Value`, // Dynamic label based on ticker
            data: stockData.map(data => data.value),
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };

    return <Line data={chartData} />;
}

export default StockGraph;
