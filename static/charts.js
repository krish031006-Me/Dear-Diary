// This is the js file that will be used for charts to be presented
document.addEventListener("DOMContentLoaded", async function(event){
    // The function of get the data via the API
    const analysisData = await getAnalysis();
    // calling to create graphs
    if (analysisData){
        console.log("inside js");
        line(analysisData);
        doughnut(analysisData);
        bar(analysisData);
    }
});

// THis is the function to interact with a Flask route and fetch the data 
async function getAnalysis(){
    try {
        const response = await fetch('/analysis');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } 
    catch (error) {
        console.error('Fetch Error:', error);
        return null; // Return null on error
    }
}

// This is the function used to create line chart()
function line(data){
    (async function(){
        // This is the new chart object
        new Chart(
            document.getElementById("line"),
            {
                type: 'line',
                data: {
                    labels: data.map(row => row["date_only"]),
                    datasets: [
                        {
                            label: "Your emotion instensity score-",
                            data: data.map(row => row["emotion_intensity"])
                        }
                    ]
                }
            }
        )
    })
}

// This function is used to create a bar graph
function bar(data){
    (async function(){
        // This is the new chart object
        new Chart(
            document.getElementById('bar'),
            {
                type: 'bar',
                data: {
                    labels: ["Happy","Sad", "Angry", "Anxious", "Calm", "Neutral", "Unknown"],
                    datasets: [
                        {
                            label: "Entries per emotion-",
                            data: [
                                data.filter(entry => entry.primary_emotion === "happy").length,
                                data.filter(entry => entry.primary_emotion === "sad").length,
                                data.filter(entry => entry.primary_emotion === "angry").length,
                                data.filter(entry => entry.primary_emotion === "anxious").length,
                                data.filter(entry => entry.primary_emotion === "calm").length,
                                data.filter(entry => entry.primary_emotion === "neutral").length,
                                data.filter(entry => entry.primary_emotion === "unknown").length,
                            ],
                            backgroundColor: ['yellow', 'blue', 'red', 'green', 'orange', 'grey', 'red']
                        }
                    ]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true}
                    }
                }
            }
        )
    })
}

// This function is to create a donut graph for representing moods
function doughnut(data){
    (async function(){
        // This is the new chart object
        new Chart(
            document.getElementById('doughnut'),
            {
                type: 'doughnut',
                data: {
                    labels: ["Happy","Sad", "Angry", "Anxious", "Calm", "Neutral", "Unknown"],
                    datasets: [
                        {
                            label: "proportions of emotions-",
                            data: [
                                data.filter(entry => entry.primary_emotion === "happy").length,
                                data.filter(entry => entry.primary_emotion === "sad").length,
                                data.filter(entry => entry.primary_emotion === "angry").length,
                                data.filter(entry => entry.primary_emotion === "anxious").length,
                                data.filter(entry => entry.primary_emotion === "calm").length,
                                data.filter(entry => entry.primary_emotion === "neutral").length,
                                data.filter(entry => entry.primary_emotion === "unknown").length,
                            ],
                            backgroundColor: ['yellow', 'blue', 'red', 'green', 'orange', 'grey', 'red'],
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    plugins: {
                        legend: {position: bottom},
                        tooltip: {enabled: true}
                    }
                }
            }
        )
    })
}