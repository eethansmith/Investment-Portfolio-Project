import React, { useState, useEffect } from 'react';

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

  return (
    <div className="historic-stock-holdings">
      <h2>Previous Stock Holdings</h2>
      {historicHoldings.map((stock, index) => (
        <div key={index} className="stock-item">
          <div className="stock-name">{stock.name || stock.ticker}</div>
          <div className="stock-details">
            <div className="gain-loss" style={{ color: stock.net_gain_loss < 0 ? 'red' : 'green' }}>
              Net Gain/Loss: ${stock.net_gain_loss.toFixed(2)}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default HistoricHoldings;
