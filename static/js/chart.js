// Stop if there is no data yet
if (!dates || dates.length === 0) {
    console.log("No chart data yet");
} else {

    // ----------------------------
    // Weight Chart
    // ----------------------------
    const weightCtx = document.getElementById("weightChart").getContext("2d");

    new Chart(weightCtx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                label: "Weight (kg)",
                data: weights,
                borderColor: "blue",
                backgroundColor: "rgba(0, 0, 255, 0.1)",
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "kg"
                    }
                }
            }
        }
    });

    // ----------------------------
    // BMI Chart
    // ----------------------------
    const bmiCtx = document.getElementById("bmiChart").getContext("2d");

    new Chart(bmiCtx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                label: "BMI",
                data: bmis,
                borderColor: "green",
                backgroundColor: "rgba(0, 128, 0, 0.1)",
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "BMI"
                    }
                }
            }
        }
    });

    // ----------------------------
    // Blood Pressure Chart
    // ----------------------------
    const bpCtx = document.getElementById("bpChart").getContext("2d");

    new Chart(bpCtx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [
                {
                    label: "Systolic (mmHg)",
                    data: systolics,
                    borderColor: "red",
                    backgroundColor: "rgba(255, 0, 0, 0.1)",
                    borderWidth: 2,
                    tension: 0.3
                },
                {
                    label: "Diastolic (mmHg)",
                    data: diastolics,
                    borderColor: "orange",
                    backgroundColor: "rgba(255, 165, 0, 0.1)",
                    borderWidth: 2,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "mmHg"
                    }
                }
            }
        }
    });

}