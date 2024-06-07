// {% extends "adminbase.html" %}

// {% block content %}
// <div class="container">
//     <h2>Requests Status Chart</h2>
//     <canvas id="statusChart"></canvas>
// </div>

// <script>
//     document.addEventListener('DOMContentLoaded', function () {
//         var ctx = document.getElementById('statusChart').getContext('2d');
//         var statusChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: {{ customer_statuses|safe }},
//                 datasets: [{
//                     label: 'Customer Requests',
//                     data: {{ customer_counts|safe }},
//                     backgroundColor: 'rgba(255, 99, 132, 0.2)',
//                     borderColor: 'rgba(255, 99, 132, 1)',
//                     borderWidth: 1
//                 }, {
//                     label: 'Technician Requests',
//                     data: {{ technician_counts|safe }},
//                     backgroundColor: 'rgba(54, 162, 235, 0.2)',
//                     borderColor: 'rgba(54, 162, 235, 1)',
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     });
// </script>
// {% endblock %}
