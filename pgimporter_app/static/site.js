$(document).ready(function () {
  'use strict'

  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });

  $('#formTableConfig').submit(function (e) {
    e.preventDefault();  // Prevent the default form submission
    // Create an object to store the key-value pairs
    let tableData = {};

    // Loop through each row and get the key-value database pairs
    $('tr[name^="db_"]').each(function () {
      let rowId = $(this).attr("name").replace("db_","");
      let rowData = {};

      rowData["hostname"] = $(this).find("input[name='hostname']").val();
      rowData["port"] = $(this).find("input[name='port'").val();
      rowData["username"] = $(this).find("input[name='username'").val();
      rowData["password"] = $(this).find("input[name='password'").val();

      tableData[rowId] = rowData;
      
    });

    //DEBUG table content
    console.log("Content of tableData:", tableData);

    // Send the data to Flask via AJAX
    $.ajax({
      type: 'POST',
      url: '/config',
      data: JSON.stringify(tableData),
      contentType: 'application/json',
      success: function (response) {
        console.log('Sent data:', response);
      },
      error: function (error) {
        console.log('Error:', error);
      }
    });
  });
});








