import React, { useState, useEffect } from 'react';

import NIO from './resources/NIO.png';

function HistoricHoldings() {
  const [historicHoldings, setHistoricHoldings] = useState([]);

  // Function to fetch historic stock holdings data
  const fetchHistoricStockHoldings = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/historic_holdings/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setHistoricHoldings(Object.values(data));
    } catch (error) {
      console.error('Fetching data failed:', error);
    }
  };

  useEffect(() => {
    fetchHistoricStockHoldings();
    const interval = setInterval(fetchHistoricStockHoldings, 2000);
    return () => clearInterval(interval);
  }, []);

    // Function to get the corresponding image based on the stock ticker
    const getImageUrl = (ticker) => {
      switch (ticker) {
        case 'NIO':
          return NIO;
        // Add cases for other tickers and their corresponding images
        default:
          return ''; // Default image or a placeholder
      }
    };

  return (
    <div className="historic-stock-holdings">
      <h2>Previous Stock Holdings</h2>
      {historicHoldings.map((stock, index) => (
        <button key={index} className="stock-button">
          <img src={getImageUrl(stock.ticker)} alt={stock.name || stock.ticker} className="stock-image" />
          <div className="stock-details">
            <div className="stock-name">{stock.name}</div>
          </div>
          <div className="stock-value-gain">
            <div className="gain-loss" style={{ color: stock.net_gain_loss < 0 ? 'red' : 'green' }}>
              ${stock.net_gain_loss.toFixed(2)}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}

export default HistoricHoldings;
