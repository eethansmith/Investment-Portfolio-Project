import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

function GraphPortfolio({ days }) {
    const [portfolioData, setPortfolioData] = useState([]);

    useEffect(() => {
        // Fetch data based on the number of days
        fetch(`http://localhost:8000/api/graph_portfolio/${days}/`)
            .then(response => response.json())
            .then(data => setPortfolioData(data))
            .catch(error => console.error('Error fetching data:', error));
    }, [days]); // Depend on 'days' to re-fetch when it changes

    const chartData = {
        labels: portfolioData.map(data => data.date),
        datasets: [
            {
                label: 'Portfolio Value',
                data: portfolioData.map(data => data.value),
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                borderWidth: 1,
                tension: 0.4,
            },
            {
                label: 'Cumulative Investment',
                data: portfolioData.map(data => data.value_paid),
                fill: false,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                borderWidth: 1,
                tension: 0.4,
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            },
            x: {
                type: 'time',
                time: {
                    unit: days <= 7 ? 'day' : 'month',
                    displayFormats: {
                        day: 'MMM D',
                        month: 'MMM YYYY'
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: true
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        animation: {
            duration: 1000
        }
    };

    return (
        <div className="portfolio-graph-container">
            <Line data={chartData} options={chartOptions} />
        </div>
    );
}

export default GraphPortfolio;