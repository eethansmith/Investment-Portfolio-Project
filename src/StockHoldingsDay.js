import React, { useState, useEffect } from 'react';

function StockHoldingsDay({ onStockSelect, timeFrame }) {
  const [holdings, setHoldings] = useState([]);
  const [images, setImages] = useState({});

  // Function to fetch data from your API
  const fetchStockHoldings = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/stock_holdings_day/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log(data);
      setHoldings(Object.values(data)); 
    } catch (error) {
      console.error('Fetching data failed:', error);
    }
  };

  // Updated handleStockClick to pass the entire stock object
  const handleStockClick = (stock) => {
    if (onStockSelect) {
      onStockSelect(stock); // Pass the entire stock object
    }
  };

  useEffect(() => {
    fetchStockHoldings();
    const interval = setInterval(fetchStockHoldings, 2000);
    return () => clearInterval(interval);
  }, [timeFrame]);

  // Function to load images
  const loadImage = async (ticker) => {
    try {
      const image = await import(`./resources/${ticker}.png`);
      return image.default;
    } catch (error) {
      // Attempt to load without '.L' if it fails
      if (ticker.endsWith('.L')) {
        try {
          const modifiedTicker = ticker.replace('.L', '');
          const image = await import(`./resources/${modifiedTicker}.png`);
          return image.default;
        } catch (innerError) {
          console.error('Error loading image:', innerError);
          return '';
        }
      }
    }
  };

  useEffect(() => {
    const loadImages = async () => {
      const loadedImages = {};
      for (const stock of holdings) {
        loadedImages[stock.ticker] = await loadImage(stock.ticker);
      }
      setImages(loadedImages);
    };

    if (holdings.length > 0) {
      loadImages();
    }
  }, [holdings]);

  useEffect(() => {
    fetchStockHoldings();
    const interval = setInterval(fetchStockHoldings, 2000);
    return () => clearInterval(interval);
  }, [timeFrame]);

  return (
    <div className="stock-holdings">
      <h2>Current Stock Holdings</h2>
      {holdings.map((stock, index) => (
        <button key={index} className="stock-button" onClick={() => handleStockClick(stock)}>
          <img src={images[stock.ticker]} alt={stock.name} className="stock-image" />
          <div className="stock-details">
            <div className="stock-name">{stock.name}</div>
            <div>{`${stock.shares_held} shares`}</div>
          </div>
          <div className="stock-value-gain">
            <div>{`$${stock.value_held.toFixed(2)}`}</div>
            <div className="gain-loss" style={{ color: stock.profit_loss_percentage < 0 ? 'red' : 'green' }}>
              {`${stock.profit_loss_percentage.toFixed(2)}%`}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}

export default StockHoldingsDay;
