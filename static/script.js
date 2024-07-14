// Particle.js configuration
particlesJS("particles-js", {
    particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: "#00fff2" },
        shape: { type: "circle" },
        opacity: { value: 0.5, random: false },
        size: { value: 3, random: true },
        line_linked: { enable: true, distance: 150, color: "#00fff2", opacity: 0.4, width: 1 },
        move: { enable: true, speed: 6, direction: "none", random: false, straight: false, out_mode: "out", bounce: false }
    },
    interactivity: {
        detect_on: "canvas",
        events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
        modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
    },
    retina_detect: true
});

document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const portfolioInput = document.getElementById('portfolio');
    const resultsDiv = document.getElementById('results');

    analyzeBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const portfolio = portfolioInput.value;
        const apiKey = '8d34eb0b88mshc982a011ac648f3p17d5c6jsn82e7b43f8ff5'; // Using the provided API key

        // Simulate loading
        resultsDiv.innerHTML = '<div class="text-center"><div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div></div>';
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ portfolio, apiKey })
            });
            
            const data = await response.json();
            
            if (data.error) {
                resultsDiv.innerHTML = `<div class="holographic-card"><p class="text-red-500">Error: ${data.error}</p></div>`;
            } else {
                // Update results
                resultsDiv.innerHTML = `
                    <div class="holographic-card">
                        <h2 class="text-2xl font-bold mb-4 glitch" data-text="Quantum Portfolio Metrics">Quantum Portfolio Metrics</h2>
                        <p class="mb-2">Mean Daily Return: <span class="text-yellow-400">${data.mean_daily_return.toFixed(6)}</span></p>
                        <p class="mb-2">Standard Deviation of Daily Returns: <span class="text-yellow-400">${data.std_dev_daily_returns.toFixed(6)}</span></p>
                        <p class="mb-2">Cumulative Returns: <span class="text-yellow-400">${data.cumulative_returns.toFixed(6)}</span></p>
                    </div>
                `;
                
                // Create chart
                createChart(data);
            }
        } catch (error) {
            resultsDiv.innerHTML = `<div class="holographic-card"><p class="text-red-500">Error: ${error.message}</p></div>`;
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
                    borderColor: 'rgb(0, 255, 242)',
                    backgroundColor: 'rgba(0, 255, 242, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(0, 255, 242)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(0, 255, 242)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: 'rgb(0, 255, 242)' } }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgb(0, 255, 242)',
                            callback: function(value) {
                                return (value * 100).toFixed(2) + '%';
                            }
                        },
                        grid: { color: 'rgba(0, 255, 242, 0.1)' }
                    },
                    x: {
                        ticks: { color: 'rgb(0, 255, 242)' },
                        grid: { color: 'rgba(0, 255, 242, 0.1)' }
                    }
                }
            }
        });
    }
});