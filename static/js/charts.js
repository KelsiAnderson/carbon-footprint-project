"use strict";

$.get('/user-emission-info.json', (res) =>{
  const labels = res.labels
  console.log(labels)
  const data = res.data
  console.log(data)
  new Chart(
    $("#myDonutChart"),
    {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data
        }]
      }
    }); 
  } 
);





