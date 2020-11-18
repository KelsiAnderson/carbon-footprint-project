"user strict";

const ctx = document.getElementById('myDonutChart')
const donutChart = new Chart(
    $('my-donut-chart'),
    
  type: 'doughnut',
  data: {
    labels: ['vehicle emissions', 'public transit', 'natural gas usage', 'electricity usage'],
    datasets: [
        {
            data: [2, 4, 8, 5]}
    ]

}); 