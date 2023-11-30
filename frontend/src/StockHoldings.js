// StockHoldings.js
import React from 'react';
import VAUG from './resources/VAUG.png'; // Adjust the path
import AAPL from './resources/AAPL.png'; // Adjust the path
import PLTR from './resources/PLTR.png'; // Adjust the path

function StockHoldings() {
  console.log('Rendering StockHoldings');
  const holdings = [
    // Replace with your actual data and images
    { name: 'S&P 500', quantity: 10, value: '$1000', imageUrl: VAUG },
    { name: 'Apple', quantity: 15, value: '$1500', imageUrl: AAPL },
    { name: 'Palantir', quantity: 15, value: '$1500', imageUrl: PLTR },
    // ... more stocks
  ];

  return (
    <div className="stock-holdings">
      <h2>My Stock Holdings</h2>
      {holdings.map((stock, index) => (
        <button key={index} className="stock-button">
          <img src={stock.imageUrl} alt={stock.name} className="stock-image" />
          <div className="stock-info">
            <div className="stock-name">{stock.name}</div>
            <div>{`${stock.quantity} shares`}</div>
            <div>{`${stock.value}`}</div>
          </div>
        </button>
      ))}
    </div>
  );
}

export default StockHoldings;
