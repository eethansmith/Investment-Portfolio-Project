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
            data: stockData.map(data => data.value),
            fill: true,
            label: '',
            backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green background
            borderColor: 'rgb(75, 192, 192)',
            borderWidth: 2,
            tension: 0.1,
            pointRadius: 0,
            hoverRadius: 0,
        }]
    };

    const chartOptions = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true // Start Y-axis at 0
            }
        },
        legend: {
            display: false // Hide the legend
        },
        tooltips: {
            mode: 'index',
            intersect: false
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        animation: {
            duration: 1000 // Animation duration in milliseconds
        }
    };


    return (
        <div className="stock-graph-container">
            <Line data={chartData} />
        </div>
    );
}

export default StockGraph;
