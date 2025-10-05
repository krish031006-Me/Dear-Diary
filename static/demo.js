// demoCharts.js
document.addEventListener("DOMContentLoaded", function () {
    // Create fake / demo data
    const demoData = createDemoData();

    // Call the graph functions with demo data
    line(demoData);
    doughnut(demoData);
    bar(demoData);
});


// This function will generate the data for all the enteries
function createDemoData() {
    const emotions = ["happy", "sad", "angry", "anxious", "calm", "neutral"];
    const demoData = [];
    const today = new Date();

    // Create data for the last 7 days
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);

        demoData.push({
            date_only: date.toISOString().split("T")[0],
            emotion_intensity: Math.floor(Math.random() * 100) + 1, // 1-10 intensity
            primary_emotion: emotions[Math.floor(Math.random() * emotions.length)]
        });
    }

    return demoData;
}

// Line Chart
function line(data) {
    new Chart(
        document.getElementById("line"),
        {
            type: 'line',
            data: {
                labels: data.map(row => row.date_only),
                datasets: [
                    {
                        label: "Demo Emotion Intensity Score",
                        data: data.map(row => row.emotion_intensity),
                        borderColor: "rgba(227, 21, 21, 1)",
                        backgroundColor: "rgba(54,162,235,0.2)",
                        tension: 0.3
                    },
                ]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, title: { display: true, text: "Intensity" } },
                    x: { title: { display: true, text: "Date" } }
                }
            }
        }
    );
}

// Bar Chart
function bar(data) {
    new Chart(
        document.getElementById("bar"),
        {
            type: 'bar',
            data: {
                labels: ["Happy", "Sad", "Angry", "Anxious", "Calm", "Neutral"],
                datasets: [
                    {
                        label: "Demo Entries per Emotion",
                        data: [
                            data.filter(entry => entry.primary_emotion === "happy").length,
                            data.filter(entry => entry.primary_emotion === "sad").length,
                            data.filter(entry => entry.primary_emotion === "angry").length,
                            data.filter(entry => entry.primary_emotion === "anxious").length,
                            data.filter(entry => entry.primary_emotion === "calm").length,
                            data.filter(entry => entry.primary_emotion === "neutral").length,
                            data.filter(entry => entry.primary_emotion === "unknown").length,
                        ],
                        backgroundColor: ['#FFD700', '#1E90FF', '#FF4500', '#32CD32', '#FFA500', '#808080', '#FF0000']
                    }
                ]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, title: { display: true, text: "Entries" } }
                }
            }
        }
    );
}

// Doughnut Chart
function doughnut(data) {
    console.log("INside doughnut");
    new Chart(
        document.getElementById("doughnut"),
        {
            type: 'doughnut',
            data: {
                labels: ["Happy", "Sad", "Angry", "Anxious", "Calm", "Neutral"],
                datasets: [
                    {
                        label: "Demo Proportions of Emotions",
                        data: [
                            data.filter(entry => entry.primary_emotion === "happy").length,
                            data.filter(entry => entry.primary_emotion === "sad").length,
                            data.filter(entry => entry.primary_emotion === "angry").length,
                            data.filter(entry => entry.primary_emotion === "anxious").length,
                            data.filter(entry => entry.primary_emotion === "calm").length,
                            data.filter(entry => entry.primary_emotion === "neutral").length
                        ],
                        backgroundColor: ['#FFD700', '#1E90FF', '#FF4500', '#32CD32', '#FFA500', '#808080', '#FF0000'],
                        borderWidth: 1
                    }
                ]
            },
            options: {
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: { enabled: true }
                }
            }
        }
    );
}
