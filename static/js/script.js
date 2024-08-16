// Auto-dismiss alerts with fade-out effect after 5 seconds
$(document).ready(function() {
    setTimeout(function() {
      $('.alert').fadeOut('slow', function() {
        $(this).alert('close');
      });
    }, 5000); // 5000 milliseconds = 5 seconds
  });