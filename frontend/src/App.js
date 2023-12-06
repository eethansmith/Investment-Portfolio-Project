// App.js or your main component file
import React, { useState } from 'react';
import './App.css';
import homeImage from './menu-con.jpg';
import StockHoldings from './StockHoldings';
import StockGraph from './StockGraphing';
import HistoricHoldings from './HistoricHoldings';

function App() {
  const [activeTab, setActiveTab] = useState('Overall Portfolio'); // default active tab
  const [selectedStock, setSelectedStock] = useState(null);

  const handleStockSelection = (stock) => {
    setSelectedStock(stock);
  };
    // Function to format the profit/loss percentage
    const formatPercentage = (percentage) => {
      if (percentage > 0) {
        return `+${percentage.toFixed(2)}%`;
      } else {
        return `${percentage.toFixed(2)}%`; // Negative values already have a minus sign
      }
    };

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
        <div className="nav-links">
          <button 
            className={activeTab === 'Overall Portfolio' ? 'active' : ''} 
            onClick={() => setActiveTab('Overall Portfolio')}
          >
            Overall Portfolio
          </button>
          <button>Overall Profits</button>
          <button>Stock Breakdown</button>
          <button>News</button>
        </div>
      </nav>
      <header className="App-header">
      <h1>{selectedStock ? `${selectedStock.name}` : 'Overall Portfolio'}</h1>
        {selectedStock && (
          <div className="stock-info">
            <p>
              Current Value: ${selectedStock.value_held.toFixed(2)}
            <span style={{ color: selectedStock.profit_loss_percentage >= 0 ? 'green' : 'red' }}>
                {` (${formatPercentage(selectedStock.profit_loss_percentage)})`}
              </span>
            </p>
            <p>Shares Held: {selectedStock.shares_held}</p>
            {/* Add other details you want to display */}
            </div>
        )}
      </header>

      {selectedStock && <StockGraph ticker={selectedStock.ticker} />}

      <StockHoldings onStockSelect={handleStockSelection} />
      <HistoricHoldings/>
      {/* Rest of your components */}
    </div>
  );
}

export default App;
