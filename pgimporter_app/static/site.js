$(document).ready(function(){
  'use strict'

  const element = document.querySelector('#navbarSideCollapse');
  if (element) {
    element.addEventListener('click', function (){
      document.querySelector('.offcanvas-collapse').classList.toggle('open')
    });
  }

});






