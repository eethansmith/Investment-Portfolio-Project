import React, { useState, useEffect } from 'react';

function HistoricHoldings() {
  const [historicHoldings, setHistoricHoldings] = useState([]);
  const [images, setImages] = useState({});


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

// Load images for all tickers when the component mounts or data changes
useEffect(() => {
  const loadImages = async () => {
    const loadedImages = {};
    for (const stock of historicHoldings) {
      loadedImages[stock.ticker] = await loadImage(stock.ticker);
    }
    setImages(loadedImages);
  };

  if (historicHoldings.length > 0) {
    loadImages();
  }
}, [historicHoldings]);

useEffect(() => {
  fetchHistoricStockHoldings();
  const interval = setInterval(fetchHistoricStockHoldings, 2000);
  return () => clearInterval(interval);
}, []);

return (
  <div className="historic-stock-holdings">
    <h2>Previous Stock Holdings</h2>
    {historicHoldings.map((stock, index) => (
      <button key={index} className="stock-button">
        <img src={images[stock.ticker]} alt={stock.name || stock.ticker} className="stock-image" />
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
