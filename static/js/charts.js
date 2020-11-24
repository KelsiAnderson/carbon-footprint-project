"use strict";

$.get('/user-emission-info.json', (res) =>{
  const labels = res.labels
  console.log(labels)
  const data = res.data
  console.log(data)
  new Chart(
    $("#currentMonthDonutChart"),
    {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data, 
          backgroundColor: ["#99ffff", "#0077ff", "#66ccff", "#335577"]
        }],
        
      }
    }); 
  } 
);


$.get('/previous-month-user-emission-info.json', (res) =>{
  const labels = res.labels
  console.log(labels)
  const data = res.data
  console.log(data)
  new Chart(
    $("#previousMonthDonutChart"),
    {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data, 
          backgroundColor: ["#99ffff", "#ff00bb", "#66ccff", "#335577"]
        }],
        
      }
    }); 
  } 
);





