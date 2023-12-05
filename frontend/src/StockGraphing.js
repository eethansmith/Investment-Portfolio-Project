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
        datasets: [
            {
                // Dataset for stock value
                label: 'Stock Value',
                data: stockData.map(data => data.value),
                fill: false,
                backgroundColor: 'rgba(75, 192, 192 0.1)',
                borderColor: 'rgb(75, 245, 192)',
                borderWidth: 0.8,
                tension: 0.1,
                pointRadius: 0,
                hoverRadius: 0,
            },
            {
                // Dataset for cumulative investment
                label: 'Cumulative Investment',
                data: stockData.map(data => data.value_paid),
                fill: false,
                
                borderColor: 'rgb(245, 245, 245)',
                borderWidth: 0.75,
                tension: 0.1,
                pointRadius: 0,
                hoverRadius: 0,
            },
        ]
    };

    const chartOptions = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true // Start Y-axis at 0
            },
            x: {
                type: 'time',
                time: {
                    unit: 'month',
                    displayFormats: {
                        month: 'DD/MM/YY'
                    }
                },
                ticks: {
                    maxTicksLimit: stockData.length / 30 // Roughly one tick per month, adjust as needed
                }
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
            duration: 2000 // Animation duration in milliseconds
        }
    };


    return (
        <div className="stock-graph-container">
            <Line data={chartData} />
        </div>
    );
}

export default StockGraph;
