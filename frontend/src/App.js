// App.js or your main component file
import React, { useState } from 'react';
import './App.css';
import homeImage from './menu-con.jpg';
import StockHoldings from './StockHoldings';
import StockGraph from './StockGraphing';

function App() {
  const [activeTab, setActiveTab] = useState('Overall Portfolio'); // default active tab
  const [selectedTicker, setSelectedTicker] = useState(null);

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
        <h1>Overall Portfolio</h1>
      </header>
      <StockHoldings/>
      { /* Add the rest of your components here */}
    </div>
  );
}

export default App;
