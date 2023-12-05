

console.log("wassup");



// document.addEventListener('DOMContentLoaded', function () {
//     var tableContainer = document.getElementById('table-container');
//     var sidebar = document.getElementById('sidebar');
//     var dataTable = document.getElementById('data-table');

//     // Function to handle row click
//     function handleRowClick(protectedData) {
//         // Update the sidebar content (customize this based on your needs)
//         // This assumes you have a function 'updateSidebarContent' that takes 'protectedData' as an argument
//         updateSidebarContent(protectedData);

//         // Shrink the table width
//         tableContainer.style.flex = '0 0 70%'; // You can adjust the width as needed

//         // Expand the sidebar width
//         sidebar.style.width = '30%'; // You can adjust the width as needed
//     }

//     // Attach click event to each row
//     var rows = document.getElementsByClassName('js-credential-row');
//     for (var i = 0; i < rows.length; i++) {
//         rows[i].addEventListener('click', function (event) {
//             var rowData = JSON.parse(event.currentTarget.getAttribute('data-protected-data'));
//             handleRowClick(rowData);
//         });
//     }
// });

// function sidebar_view(protected_data){
//     console.log(protected_data);
//     console.log(protected_data.service_name)
//     document.querySelector('.js-sidebar').innerHTML = `
//         <td>${protected_data.service_name}</td>
//         <td>${protected_data.service_username}</td>
//         <td>${protected_data.service_password}</td>
//         <td>${protected_data.created_by}</td>
//         <td>${protected_data.created_date}</td>`;
// }

