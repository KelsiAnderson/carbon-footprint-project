"use strict";

$.get('/user-emission-info.json', (res) =>{
  const data = []
  for (const info of res.data){
    data.push({monthly_elect: info.month_elect,
              vehicle_emit: vehicle_emit,
              nat_gas_emit: nat_gas_emit,
              public_trans_emit: public_trans_emit
    })  // end data push
  } // end for
  new Chart($("#myDonutChart"),
   {
    
    type: 'doughnut',
    data: {
      labels: ['electricity usage', 'vehicle emissions', 'natural gas usage', 'public transit' ],
      datasets: [{
        data: data
      }]
    }
  }); 

  
}
)
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
//       data: data
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