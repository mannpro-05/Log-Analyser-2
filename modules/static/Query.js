// --------------------------------navigation-----------------------------------------
$(document).ready(function () {
    $('.menu-toggle').click(function () {
      $('.menu-toggle').toggleClass('active')
      $('nav').toggleClass('active')
    })
  })
// --------------------------------navigation-----------------------------------------


function sendQuery(){
    var data = {
        "subject" : $("#subject").val(),
        "body" : $("#message").val()
    }
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/sendQuery'

    }).done(function (data) {
        alert(data.message);
    })
}