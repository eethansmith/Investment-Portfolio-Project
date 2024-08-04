import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import 'chartjs-adapter-date-fns';

function AllGraphDay({ ticker, timeFrame }) {
    const [stockData, setStockData] = useState([]);

    useEffect(() => {
        // Ensure the ticker value is included in the fetch URL
        fetch(`http://localhost:8000/api/graph_all_day/`)
            .then(response => response.json())
            .then(data => setStockData(data))
            .catch(error => console.error('Error fetching data:', error));
    }, [ticker]);

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
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                mode: 'index',
                intersect: false
            },
        },
        scales: {
            y: {
                beginAtZero: false 
            },
            x: {
                type: 'time',
                time: {
                    unit: 'month',
                    displayFormats: {
                        month: 'dd-MM-yy-HH:mm'
                    }
                },
                ticks: {
                    display: false
                }
            }
        },
        animation: {
            duration: 1000 // Animation duration in milliseconds
        }
    };


    return (
        <div className="stock-graph-container">
            <Line data={chartData} options={chartOptions} />
        </div>
    );
}

export default AllGraphDay;
