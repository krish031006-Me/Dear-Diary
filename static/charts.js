// charts.js – scroll-triggered version
document.addEventListener("DOMContentLoaded", async function () {
    const analysisData = await getAnalysis();
    console.log(analysisData);
    if (analysisData && analysisData.length > 0) {
        console.log("✅ Data ready for charts:", analysisData);

        // Observe charts for scroll-triggered animation
        observeChart('line', () => line(analysisData));
        observeChart('bar', () => bar(analysisData));
        observeChart('doughnut', () => doughnut(analysisData));

    } else {
        console.warn("No analysis data to display.");
    }
});

// --- Fetch data from Flask route ---
async function getAnalysis() {
    try {
        const response = await fetch('/analysis');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const rawData = await response.json();

        const entries = Object.values(rawData);
        return entries;
    } catch (error) {
        console.error("Fetch Error:", error);
        return [];
    }
}

// --- Intersection Observer for scroll-triggered charts ---
function observeChart(canvasId, createChartFunc) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                createChartFunc();       // Create the chart when visible
                obs.unobserve(canvas);   // Stop observing after first animation
            }
        });
    }, { threshold: 0.9 }); // 50% visible

    observer.observe(canvas);
}

// --- Line Chart ---
function line(data) {
    new Chart(
        document.getElementById("line"),
        {
            type: 'line',
            data: {
                labels: data.map(entry => entry.date_created),
                datasets: [{
                    label: "Your emotion intensity score",
                    data: data.map(entry => entry.emotion_intensity || 0),
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0, 0, 255, 0.2)',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                animation: { duration: 1000 },
                scales: { y: { beginAtZero: true } }
            }
        }
    );
}

// --- Bar Chart ---
function bar(data) {
    const emotions = ["happy", "sad", "angry", "anxious", "calm", "neutral", "unknown"];
    new Chart(
        document.getElementById('bar'),
        {
            type: 'bar',
            data: {
                labels: emotions.map(e => e.charAt(0).toUpperCase() + e.slice(1)),
                datasets: [{
                    label: "Entries per emotion",
                    data: emotions.map(emotion =>
                        data.filter(entry => entry.primary_emotion === emotion).length
                    ),
                    backgroundColor: ['#FFD700', '#1E90FF', '#FF4500', '#32CD32', '#FFA500', '#808080', '#FF69B4']
                }]
            },
            options: {
                responsive: true,
                animation: { duration: 1000 },
                scales: { y: { beginAtZero: true } }
            }
        }
    );
}

// --- Doughnut Chart ---
function doughnut(data) {
    const emotions = ["happy", "sad", "angry", "anxious", "calm", "neutral", "unknown"];
    new Chart(
        document.getElementById('doughnut'),
        {
            type: 'doughnut',
            data: {
                labels: emotions.map(e => e.charAt(0).toUpperCase() + e.slice(1)),
                datasets: [{
                    label: "Proportions of emotions",
                    data: emotions.map(emotion =>
                        data.filter(entry => entry.primary_emotion === emotion).length
                    ),
                    backgroundColor: ['#FFD700', '#1E90FF', '#FF4500', '#32CD32', '#FFA500', '#808080', '#FF69B4'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                animation: { duration: 1000 },
                plugins: { legend: { position: 'bottom' }, tooltip: { enabled: true } }
            }
        }
    );
}
