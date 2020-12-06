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
          backgroundColor: ["#338800", "#9999ff", "#00cc33", "#0033cc"]
        }],
      },
      options: {legend:
        {labels: 
          {fontColor: 'white', fontStyle: 'bold', fontFamily: 'Montserrat'},
        }
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
          backgroundColor: ["#99ffff", "#0033cc", "#66ccff", "#00cc33"]
        }],  
      },
      options: {legend:
        {labels: 
          {fontColor: 'white', fontStyle: 'bold', fontFamily: 'Montserrat'},
        }
      }
    }); 
  } 
);





