// Weight Chart
const weightCtx = document.getElementById("weightChart").getContext("2d");

new Chart(weightCtx, {
    type: "line",
    data: {
        labels: dates,
        datasets: [{
            label: "Weight (kg)",
            data: weights,
            borderWidth: 2
        }]
    }
});

// BMI Chart
const bmiCtx = document.getElementById("bmiChart").getContext("2d");

new Chart(bmiCtx, {
    type: "line",
    data: {
        labels: dates,
        datasets: [{
            label: "BMI",
            data: bmis,
            borderWidth: 2
        }]
    }
});