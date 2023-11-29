import React, { useState, useEffect } from 'react';
import axios from 'axios';

function StockHoldings() {
    const [holdings, setHoldings] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/stock_holdings/') // Update with your API endpoint
            .then(response => {
                setHoldings(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the stock holdings:', error);
            });
    }, []);

    // Function to dynamically import images based on the ticker symbol
    const getStockImage = (tickerSymbol) => {
        try {
            return require(`./resources/${tickerSymbol}.png`);
        } catch (e) {
            console.warn(`Image not found for ticker symbol: ${tickerSymbol}`);
            return ''; // return a default image or empty string
        }
    }

    return (
        <div className="stock-holdings">
            <h2>My Stock Holdings</h2>
            {holdings.map((stock, index) => (
                <button key={index} className="stock-button">
                    <img 
                        src={getStockImage(stock['Ticker Symbol'])} 
                        alt={stock['Ticker Symbol']} 
                        className="stock-image" 
                    />
                    <div className="stock-info">
                        <div className="stock-name">{stock['Ticker Symbol']}</div>
                        <div>{`${stock['No. of Shares']} shares`}</div>
                        <div>{`$${stock['Price per Share USD']}`}</div>
                    </div>
                </button>
            ))}
        </div>
    );
}

export default StockHoldings;
