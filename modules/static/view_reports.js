// --------------------------------navigation-----------------------------------------
$(document).ready(function () {
    $('.menu-toggle').click(function () {
      $('.menu-toggle').toggleClass('active')
      $('nav').toggleClass('active')
    })
  })
// --------------------------------navigation-----------------------------------------

function myDownloadFunction(){
    alert("The file which you asked for is being created so please wait. The download will begin shortly.")
}


function confirmAction() {
    let confirmAction = confirm("Are You Sure To Delete The Record?");
    if (confirmAction) {
      alert("successfully Deleted");
    } else {
      alert("Action canceled");
    }
  }



$(document).ready(function() {


    window.onclick = function(event) {
        if (!event.target.matches('.dropdownbutton')) {

            $(".dropdown-content").each(function(){
                $(this).hide();
            });
        }
    }

    console.log("Ready");
});



function dropdownControl(downloadDropdown){
    $(downloadDropdown).parent().find(".dropdown-content").toggle("show");
}

function downloadReport(downloadButton,format){
    var data = {
        "title": $(downloadButton).closest("tr").find(".reportTitle").text(),
        "fileType": format
    }

    console.log("Download: ",data);

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'text/csv',
        url: '/download',
    })
}

function deleteReport(deleteButton){
    var data = {
        "title": $(deleteButton).closest("tr").find(".reportTitle").text()
    }

    console.log("Delete: ",data);

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/deleteReport',
    }).done(function (data) {
        if (data.delete === "yes"){
            $(deleteButton).parents("tr").remove();
            alert(data.message);
        }
        else {
            alert(data.message);
        }

    });

}