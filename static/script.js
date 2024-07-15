document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const portfolioInput = document.getElementById('portfolio');
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const resultsDiv = document.getElementById('results');

    analyzeBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const portfolio = portfolioInput.value;
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const apiKey = '8d34eb0b88mshc982a011ac648f3p17d5c6jsn82e7b43f8ff5';

        resultsDiv.innerHTML = '<div class="text-center"><div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div></div>';

        console.log('Sending request to /analyze with data:', { portfolio, apiKey, startDate, endDate });

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ portfolio, apiKey, startDate, endDate })
            });

            const data = await response.json();
            console.log('Response received from /analyze:', data);

            if (data.error) {
                resultsDiv.innerHTML = `<div class="bg-white shadow-lg rounded-lg p-4"><p class="text-red-500">Error: ${data.error}</p></div>`;
            } else {
                resultsDiv.innerHTML = `
                    <div class="bg-white shadow-lg rounded-lg p-8">
                        <h2 class="text-2xl font-bold mb-4">Quantum Portfolio Metrics</h2>
                        <p class="mb-2">Mean Daily Return: <span class="text-blue-500">${data.mean_daily_return.toFixed(6)}</span></p>
                        <p class="mb-2">Standard Deviation of Daily Returns: <span class="text-blue-500">${data.std_dev_daily_returns.toFixed(6)}</span></p>
                        <p class="mb-2">Cumulative Returns: <span class="text-blue-500">${data.cumulative_returns.toFixed(6)}</span></p>
                    </div>
                `;
                createChart(data);
            }
        } catch (error) {
            console.error('Error during fetch request:', error);
            resultsDiv.innerHTML = `<div class="bg-white shadow-lg rounded-lg p-4"><p class="text-red-500">Error: ${error.message}</p></div>`;
        }
    });

    function createChart(data) {
        const chartContainer = document.getElementById('chartContainer');
        chartContainer.innerHTML = '<canvas id="portfolioChart"></canvas>';
        const ctx = document.getElementById('portfolioChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1 Month', '3 Months', '6 Months', '1 Year'],
                datasets: [{
                    label: 'Quantum Cumulative Returns',
                    data: [
                        data.cumulative_returns * 0.25,
                        data.cumulative_returns * 0.5,
                        data.cumulative_returns * 0.75,
                        data.cumulative_returns
                    ],
                    borderColor: 'rgb(0, 119, 182)',
                    backgroundColor: 'rgba(0, 119, 182, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(0, 119, 182)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(0, 119, 182)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: 'rgb(0, 119, 182)' } }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgb(0, 119, 182)',
                            callback: function (value) {
                                return (value * 100).toFixed(2) + '%';
                            }
                        },
                        grid: { color: 'rgba(0, 119, 182, 0.1)' }
                    },
                    x: {
                        ticks: { color: 'rgb(0, 119, 182)' },
                        grid: { color: 'rgba(0, 119, 182, 0.1)' }
                    }
                }
            }
        });
    }
});
