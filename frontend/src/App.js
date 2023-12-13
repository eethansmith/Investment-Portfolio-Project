import React, { useEffect, useState } from 'react';
import './App.css';
import homeImage from './resources/menu-con.jpg';
import StockHoldings from './StockHoldings';
import StockGraphAll from './StockGraphingAll';
import StockGraphDay from './StockGraphingDay';
import HistoricHoldings from './HistoricHoldings';
import TimeFrameFlip from './TimeFrameFlip';

function App() {
  const [selectedStock, setSelectedStock] = useState(null);
  const [timeFrame, setTimeFrame] = useState('All');

  const handleStockSelection = (stock) => {
    setSelectedStock(stock);
  };

  const handleTimeFrameChange = (newTimeFrame) => {
    setTimeFrame(newTimeFrame);
  };

  // Function to format the profit/loss percentage
  const formatPercentage = (percentage) => {
    if (percentage > 0) {
      return `+${percentage.toFixed(2)}%`;
    } else {
      return `${percentage.toFixed(2)}%`; // Negative values already have a minus sign
    }
  };

  const fetchSelectedStockData = async () => {
    if (selectedStock) {
      try {
        const response = await fetch(`[Your API Endpoint]/${selectedStock.ticker}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // Update your selectedStock state with the new data
        setSelectedStock(data);
      } catch (error) {
        console.error('Fetching stock data failed:', error);
      }
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetchSelectedStockData();
    }, 5000); 
    return () => clearInterval(interval);
  }, [selectedStock]);

  return (
    <div className="App">
      <nav className="App-nav">
        <div className="home-button">
          <img src={homeImage} alt="Home" />
          <span className="home-text">Home</span>
        </div>
        <div className="project-title">
          Investment Portfolio
        </div>
        {/* Removed activeTab and setActiveTab related code from nav-links */}
        <div className="nav-links">
          <button>Portfolio</button>
          <button>Overall Profits</button>
          <button>Stock Breakdown</button>
          <button>News</button>
        </div>
      </nav>
      <header className="App-header">
        <div className="header-content">
        <div className="title-container">
        <h1>{selectedStock ? `${selectedStock.name}` : 'Overall Portfolio'}</h1>
        </div>
          <TimeFrameFlip onTimeFrameChange={handleTimeFrameChange} currentTimeFrame={timeFrame} />
          </div>
          {selectedStock && (
            <div className="stock-info">
              <p>
                Current Value: ${selectedStock.value_held.toFixed(2)}
                
                <span style={{ color: selectedStock.profit_loss_percentage >= 0 ? 'green' : 'red' }}>
                  {` (${formatPercentage(selectedStock.profit_loss_percentage)})`}
                </span>
              </p>
              <p>Shares Held: {selectedStock.shares_held}</p>
            </div>
        )}
      </header>
      {/* The overall graphing component and its related code have been removed */}
      {selectedStock && timeFrame === 'All' && <StockGraphAll ticker={selectedStock.ticker} timeFrame={timeFrame} />}
      {selectedStock && timeFrame === 'Day' && <StockGraphDay ticker={selectedStock.ticker} timeFrame={timeFrame} />}
      <StockHoldings onStockSelect={handleStockSelection} timeFrame={timeFrame} />
      <HistoricHoldings/>
      {/* Rest of your components */}
    </div>
  );
}

export default App;
