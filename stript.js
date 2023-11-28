document.addEventListener('DOMContentLoaded', function() {
    // Assuming your JSON data is stored locally in a file named `data.json`
    fetch('investments_data.json')
        .then(response => response.json())
        .then(data => {
            displayData(data);
        })
        .catch(error => console.error('Error:', error));
});

function displayData(data) {
    const container = document.getElementById('portfolioContainer');
    let table = '<table><tr><th>Date</th><th>Ticker Symbol</th><th>Transaction Type</th><th>No. of Shares</th><th>Price per Share</th><th>Total Value</th></tr>';

    data.forEach(item => {
        table += `<tr>
                    <td>${item.Date}</td>
                    <td>${item['Ticker Symbol']}</td>
                    <td>${item['Transaction Type']}</td>
                    <td>${item['No. of Shares']}</td>
                    <td>${item['Price per Share USD']}</td>
                    <td>${(parseFloat(item['No. of Shares']) * parseFloat(item['Price per Share USD'].replace('$', ''))).toFixed(2)}</td>
                  </tr>`;
    });

    table += '</table>';
    container.innerHTML = table;
}
