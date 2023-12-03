import React from 'react';
// Import images - adjust the path as needed
import VAUG from './resources/VAUG.png';
import AAPL from './resources/AAPL.png';
import PLTR from './resources/PLTR.png';

function StockHoldings() {
  console.log('Rendering StockHoldings');
  const holdings = [
    // Update this with your actual data, images, and gain/loss info
    { name: 'S&P 500', shares: 10, value: '$1000', gainLoss: '+5%', imageUrl: VAUG },
    { name: 'Apple', shares: 15, value: '$1500', gainLoss: '+3%', imageUrl: AAPL },
    { name: 'Palantir', shares: 15, value: '$1500', gainLoss: '-2%', imageUrl: PLTR },
    // ... more stocks
  ];

  return (
    <div className="stock-holdings">
      <h2>My Stock Holdings</h2>
      {holdings.map((stock, index) => (
        <button key={index} className="stock-button">
          <img src={stock.imageUrl} alt={stock.name} className="stock-image" />
          <div className="stock-details">
            <div className="stock-name">{stock.name}</div>
            <div>{`${stock.shares} shares`}</div>
          </div>
          <div className="stock-value-gain">
            <div>{stock.value}</div>
            <div className="gain-loss" style={{ color: stock.gainLoss.startsWith('-') ? 'red' : 'green' }}>
              {stock.gainLoss}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}
export default StockHoldings;
