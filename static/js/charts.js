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
  } // end for
);
// emission_info = [{
//   "monthly_elect": monthly_elect,
//   "vehicle_emit": vehicle_emit,
//   "nat_gas_emit": nat_gas_emit,
//   "public_trans_emit": public_trans_emit
// }]

// const ctx = document.getElementById('myDonutChart')

// const donutChart = new Chart(ctx, {
//   type: 'doughnut',
//   data: {
//     labels: ['electricity usage', 'vehicle emissions', 'natural gas usage', 'public transit' ],
//     datasets: [{
//       data: [2, 4, 7, 12]
//     }]
//   }
// }); 




// const testChart = new Chart(
//     $('#myDonutChart'),
//     {
//       type: 'bar',
//       data: {
//         labels: ['does', 'this', 'work'],
//         datasets: [
//           {data: [2, 4, 8]}
//         ]
//       }
//     }
//   );