const emailRow = `
<tr>
    <td>
        <input class="inputRecipient" type="email" name="inputRecipient">
        <b><small class="ErrorContainer">Error Message</small></b>
    </td>
    <td>
        <select onchange="frequencyChange(this)" class="Frequency" name="Frequency">
            <option value="Daily">Daily</option>
            <option value="Weekly">Weekly</option>
            <option value="Monthly">Monthly</option>
        </select>
    </td>
    <td>
        <input class="time" type="time" name="time" value="17:00">
        <select style="display:none;" class="Dates" name="Dates">
            <option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option><option value="23">23</option><option value="24">24</option><option value="25">25</option><option value="26">26</option><option value="27">27</option><option value="28">28</option>
        </select>
        <select style="display:none;" class="SelectWeek" name="SelectWeek">
            <option value="Monday">Monday</option>
            <option value="Tuesday">Tuesday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thursday">Thursday</option>
            <option value="Friday">
                Friday
            </option>
            <option value="Saturday">
                Saturday
            </option>
            <option value="Sunday">
                Sunday
            </option>
        </select>
    </td>
    <td>
        <button onclick="removeRow(this)" name="DeleteRow" class="RemoveButton" >
            <i class="fa fa-trash"></i>
        </button>
    </td>
</tr>
`;
const filterRow = `
<tr>
    <td>
        <select onchange="filterChange(this)" class="filterColumn" name="FilterOptions">
            <option value="STATUS">STATUS</option>
            <option value="UPLOAD">UPLOAD</option>
            <option value="DOWNLOAD">DOWNLOAD</option>
            <option value="CLIENT_IP">CLIENT_IP</option>
            <option value="USERNAME" selected>USERNAME</option>
            <option value="METHOD">METHOD</option>
            <option value="URL">URL</option>
            <option value="HTTP_REFERER">HTTP_REFERER</option>
            <option value="USERAGENT">USERAGENT</option>
            <option value="FILTER_NAME">FILTER_NAME</option>
            <option value="FILTER_REASON">FILTER_REASON</option>
            <option value="CACHECODE">CACHECODE </option>
            <option value="USER_GROUPS">USER_GROUPS</option>
            <option value="REQUEST_PROFILES">REQUEST_PROFILES</option>
            <option value="APPLICATION_SIGNATURES">APPLICATION_SIGNATURES</option>
            <option value="CATEGORIES">CATEGORIES</option>
            <option value="UPLOAD_CONTENT">UPLOAD_CONTENT</option>
            <option value="DOWNLOAD_CONTENT">DOWNLOAD_CONTENT</option>
        </select>
    </td>
    <td>
        <select class="filterCondition" name="filterConditionSelect">
            <option value="=">Equals</option>
            <option value="!=">Not Equals</option>
        </select>
    </td>
    <td>
        <div class="filterValue" name="filterValue">
            <div class="magicSuggest" name="magicSuggest">
            </div>
            <b><small class="ErrorContainer">Error Message</small></b>
        </div>
    </td>
    <td>
        <button onclick="removeRow(this)" name="DeleteRow" class="RemoveButton"><i class="fa fa-trash"></i></button>
    </td>
</tr>
`;

var sampleData = [
    { 'METHOD': 'GET', 'DOWNLOAD': '0', 'UPLOAD': '120', 'STATUS': '200', 'DATE_TIME': '21/jul/2018:19:58:26', 'USERNAME': 'Kishan@456:456:465:45', 'CLIENT_IP': '456:456:465:45', 'URL': 'http://example.com', 'HTTP_REFERER': 'http://example.com', 'USERAGENT': 'Chrome', 'FILTER_NAME': 'DLP', 'FILTER_REASON': 'application/vnd.ms-excel', 'CACHECODE': 'TCP_DENIED', 'USER_GROUPS': '', 'REQUEST_PROFILES': '""', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,Firefox,Internet Browser', 'CATEGORIES': 'Search Engines & Portals', 'UPLOAD_CONTENT': 'application/vnd.ms-word,text/plain', 'DOWNLOAD_CONTENT': 'image/png' },
    { 'METHOD': 'POST', 'DOWNLOAD': '626', 'UPLOAD': '0', 'STATUS': '203', 'DATE_TIME': '22/Oct/2019:18:52:55', 'USERNAME': 'poriya@10:0:2:45', 'CLIENT_IP': '10:0:2:45', 'URL': 'http://website.com', 'HTTP_REFERER': 'http://192.26.25.54', 'USERAGENT': 'Monzila', 'FILTER_NAME': '-', 'FILTER_REASON': '-', 'CACHECODE': 'TCP_MISS', 'USER_GROUPS': 'office 1', 'REQUEST_PROFILES': 'MEDIUM UPLOAD', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,All Posts,All Uploads,Uploads,Firefox,Internet Browser', 'CATEGORIES': 'Unknown', 'UPLOAD_CONTENT': 'app/vnd.ms-ppt,text/plain', 'DOWNLOAD_CONTENT': 'image/jpg' },
    { 'METHOD': 'GET', 'DOWNLOAD': '235', 'UPLOAD': '125478', 'STATUS': '150', 'DATE_TIME': '23/Jan/2020:15:56:52', 'USERNAME': 'aditya@192:56:40:48', 'CLIENT_IP': '192:56:40:48', 'URL': 'http://google.com', 'HTTP_REFERER': 'http://poki.com', 'USERAGENT': 'Safari', 'FILTER_NAME': 'DLP', 'FILTER_REASON': '-', 'CACHECODE': 'TCP_MISS', 'USER_GROUPS': 'offiece 2', 'REQUEST_PROFILES': 'MEDIUM UPLOAD', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,All Posts,Uploads,Firefox,Internet Browser', 'CATEGORIES': 'Portals', 'UPLOAD_CONTENT': 'data/vnd.ms-excel,text/plain', 'DOWNLOAD_CONTENT': 'image/jpeg' },
    { 'METHOD': 'DELETE', 'DOWNLOAD': '452', 'UPLOAD': '45215', 'STATUS': '200', 'DATE_TIME': '24/Feb/2015:01:15:20', 'USERNAME': 'rishi@192:78:12:56', 'CLIENT_IP': '192:78:12:56', 'URL': 'http://sitechecker.com', 'HTTP_REFERER': 'http://459.21.25.23', 'USERAGENT': 'AppleWEbKit', 'FILTER_NAME': '-', 'FILTER_REASON': 'application/vnd.ms-word', 'CACHECODE': 'TCP_MISS', 'USER_GROUPS': 'office 3', 'REQUEST_PROFILES': 'MEDIUM UPLOAD', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,Uploads,Firefox,Internet Browser', 'CATEGORIES': 'Search Engines', 'UPLOAD_CONTENT': 'file/vnd.ms-html,text/plain', 'DOWNLOAD_CONTENT': 'audio/mp3' },
    { 'METHOD': 'PUT', 'DOWNLOAD': '452', 'UPLOAD': '035422', 'STATUS': '403', 'DATE_TIME': '20/Apr/2020:20:51:32', 'USERNAME': 'rishikesh@192:45:75:45', 'CLIENT_IP': '192:45:75:45', 'URL': 'http://twitter.com', 'HTTP_REFERER': 'http://twit.com', 'USERAGENT': 'Monzila', 'FILTER_NAME': '-', 'FILTER_REASON': 'application/vnd.ms-ppt', 'CACHECODE': 'TCP_DENIED', 'USER_GROUPS': 'office 4', 'REQUEST_PROFILES': '""', 'APPLICATION_SIGNATURES': 'non', 'CATEGORIES': 'Unknown', 'UPLOAD_CONTENT': 'application/vnd.ms-css,text/plain', 'DOWNLOAD_CONTENT': 'video/mp4' },
    { 'METHOD': 'POST', 'DOWNLOAD': '254', 'UPLOAD': '45213681', 'STATUS': '203', 'DATE_TIME': '05/March/2019:12:24:36', 'USERNAME': 'prathamesh@192:255:255:10', 'CLIENT_IP': '192:255:255:10', 'URL': 'http://facebok.com', 'HTTP_REFERER': 'http://facbk.com', 'USERAGENT': 'Ubuntu', 'FILTER_NAME': '-', 'FILTER_REASON': '-', 'CACHECODE': 'TCP_MISS', 'USER_GROUPS': 'office 5', 'REQUEST_PROFILES': '""', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,Firefox,Internet Browser', 'CATEGORIES': 'Search', 'UPLOAD_CONTENT': 'Template/vnd.ms-excel,text/plain', 'DOWNLOAD_CONTENT': 'audio/mp4' },
    { 'METHOD': 'GET', 'DOWNLOAD': '021', 'UPLOAD': '032156', 'STATUS': '150', 'DATE_TIME': '16/May/2014:15:23:20', 'USERNAME': 'varad@192:225:225:256', 'CLIENT_IP': '192:225:225:256', 'URL': 'http://snapchat.com', 'HTTP_REFERER': 'http://Snpcht.com', 'USERAGENT': 'Linux', 'FILTER_NAME': 'DLP', 'FILTER_REASON': '-', 'CACHECODE': 'TCP_MISS', 'USER_GROUPS': 'office 6', 'REQUEST_PROFILES': 'MEDIUM UPLOAD', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,Firefox,Internet Browser', 'CATEGORIES': 'Search Engines & Portals', 'UPLOAD_CONTENT': '-', 'DOWNLOAD_CONTENT': 'image/png/jpeg' },
    { 'METHOD': 'POST', 'DOWNLOAD': '154', 'UPLOAD': '512021', 'STATUS': '102', 'DATE_TIME': '19/july/2010:11:15:35', 'USERNAME': 'ridhish@192:568:568:56', 'CLIENT_IP': '192:568:568:56', 'URL': 'http://whatsapp.com', 'HTTP_REFERER': 'http://whsapp.com', 'USERAGENT': 'Firefox', 'FILTER_NAME': 'DLP', 'FILTER_REASON': 'application/vnd.ms-excel', 'CACHECODE': 'TCP_DENIED', 'USER_GROUPS': 'office 7', 'REQUEST_PROFILES': 'MEDIUM UPLOAD', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,All Posts,All Uploads,Firefox,Internet Browse', 'CATEGORIES': 'Search Engines & Portals', 'UPLOAD_CONTENT': '-', 'DOWNLOAD_CONTENT': 'img/raw' },
    { 'METHOD': 'POST', 'DOWNLOAD': '658', 'UPLOAD': '000', 'STATUS': '205', 'DATE_TIME': '03/Aug/2016:23:25:35', 'USERNAME': 'jay@192:482:489:78', 'CLIENT_IP': '192:482:489:78', 'URL': 'http://chrome.com', 'HTTP_REFERER': 'http://chr.com', 'USERAGENT': 'google', 'FILTER_NAME': 'DLP', 'FILTER_REASON': '-', 'CACHECODE': 'TCP_DENIED', 'USER_GROUPS': 'office 8', 'REQUEST_PROFILES': '""', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,All Uploads,Uploads,Firefox,Internet Browse', 'CATEGORIES': 'Search Engines', 'UPLOAD_CONTENT': 'animation/vnd.ms-excel,text/plain', 'DOWNLOAD_CONTENT': 'image/eps' },
    { 'METHOD': 'GET', 'DOWNLOAD': '125', 'UPLOAD': '4512584', 'STATUS': '400', 'DATE_TIME': '15/Oct/2016:08:22:45', 'USERNAME': 'kk@192:412:311:54', 'CLIENT_IP': '192:412:311:54', 'URL': 'http://monzila.com', 'HTTP_REFERER': 'http://459.789.161.45', 'USERAGENT': 'chrome', 'FILTER_NAME': '-', 'FILTER_REASON': '-', 'CACHECODE': 'TCO_MISS', 'USER_GROUPS': 'office 9', 'REQUEST_PROFILES': 'MEDIUM UPLOAD', 'APPLICATION_SIGNATURES': 'Unidentified Web2.0,All Posts,Uploads,Firefox,Internet Browse', 'CATEGORIES': 'Search Engines & Unknown', 'UPLOAD_CONTENT': 'application/vnd.ms-excel,text/plain', 'DOWNLOAD_CONTENT': 'img/gif' }
];

var numberInput = '<input class="numberFilter" type="number" name="magicSuggest[]" min="0" ></input>';
var hugeFilterValueInput = '<input class="hugeFilter" type="text" name="magicSuggest[]"></input>';

var numericFilterArray = ["STATUS", "UPLOAD", "DOWNLOAD"];
var hugeFilterValueArray = ["URL", "HTTP_REFERER"];
var numericFilterOptions = {
    "Greater Than": ">",
    "Less Than": "<",
    // "Between": "between",
};
var selectedColumns = ["DATE_TIME", "USERNAME", "CLIENT_IP"];
var columnOptions = ["DATE_TIME", "STATUS", "UPLOAD", "DOWNLOAD", "CLIENT_IP", "USERNAME", "METHOD", "URL", "HTTP_REFERER", "USERAGENT", "FILTER_NAME", "FILTER_REASON", "CACHECODE", "USER_GROUPS", "REQUEST_PROFILES", "APPLICATION_SIGNATURES", "CATEGORIES", "UPLOAD_CONTENT", "DOWNLOAD_CONTENT"];
var noFilterRows = 0
var magicsuggs = [];

$(document).ready(function () {
    $('.menu-toggle').click(navigationToggle);
    setColumnDropdown();
    $('#columnDropdown').on("change", columnDropdownFunction);
    $("#columnButton").click(columnButtonFunction);
    buildPreviewTable();
    $("#AddEmailRow").click(addEmailRow);
    $("#AddFilterRow").click(addFilterRow);
    console.log("Ready");
});

function navigationToggle(){
    $('.menu-toggle').toggleClass('active');
    $('nav').toggleClass('active');
}

function setColumnDropdown() {
    $.each(columnOptions, function (key, col) {
        $('#columnDropdown').append(
            $('<option></option>').val(col).html(col)
        );
    });
}

function columnDropdownFunction() {
    console.log($("#columnDropdown").val(), selectedColumns);
    if (jQuery.inArray($("#columnDropdown").val(), selectedColumns) != -1) {
        $("#columnButton").text("Remove");
        $("#columnButton").css('background-color', 'rgb(255, 79, 79)');
    }
    else {
        $("#columnButton").text("Add");
        $("#columnButton").css('background-color', '#85ec37');
    }

}

function columnButtonFunction() {

    if ($("#columnButton").text() == "Add") {
        console.log("Add ", $("#columnDropdown").val());
        $("#columnButton").css('background-color', 'rgb(255, 79, 79)');
        addColumn($("#columnDropdown").val());
    }
    else {
        console.log("Remove ", $("#columnDropdown").val());
        $("#columnButton").css('background-color', '#85ec37');
        removeColumn($("#columnDropdown").val());
    }
}

function buildPreviewTable() {

    // Clear the table
    $("#PreviewTable").empty();

    // Add the heading
    var headerRow = '<thead><tr class="bg-info">';
    $.each(selectedColumns, function (key, col) {
        headerRow += "<th>" + col + "</th>"
    });

    headerRow += "</tr></thead>";
    $("#PreviewTable").append(headerRow);

    // Add Data
    $("#PreviewTable").append("<tbody>");
    $.each(sampleData, function (key, dataRow) {
        var row = "<tr>";

        $.each(selectedColumns, function (key, col) {
            row += "<td>" + dataRow[col] + "</td>";
        });

        row += "</tr>";
        $("#PreviewTable").append(row);

    });
    $("#PreviewTable").append("</tbody>");
}

function addColumn(columnName) {
    selectedColumns.push(columnName);
    $("#columnButton").text("Remove");
    buildPreviewTable();
}

function removeColumn(columnName) {

    selectedColumns = jQuery.grep(selectedColumns, function (value) {
        return value != columnName;
    });

    console.log(selectedColumns);
    $("#columnButton").text("Add");
    buildPreviewTable();
}

function frequencyChange(frequencySelect) {
    let scheduleTD = $(frequencySelect).closest('td').next('td');
    switch ($(frequencySelect).val()) {
        case "Daily":
            scheduleTD.find('.Dates').hide();
            scheduleTD.find('.SelectWeek').hide();
            break;
        case "Weekly":
            scheduleTD.find('.Dates').hide();
            scheduleTD.find('.SelectWeek').show();
            break;
        case "Monthly":
            scheduleTD.find('.Dates').show();
            scheduleTD.find('.SelectWeek').hide();
            break;
    }
}

function addEmailRow() {
    $("#EmailTable tbody").append(emailRow);
}

function removeRow(row) {
    $(row).parents("tr").remove();
}

function addFilterRow() {

    var row = $("#FilterTable tbody").append(filterRow);
    var TargetColumn = $(row).find(".filterColumn").val();
    $(row).find("tr").last().attr('id', "filterRow-" + noFilterRows);
    var magicData = null;
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ filter: TargetColumn }),
        dataType: 'json',
        url: '/getMagicSuggestData',
        async: false,
        success : function(data) {
                    magicData = data;
                    console.log(magicData);
                }

    });
    console.log(magicData);
    $(row).find(".filterValue .magicSuggest").magicSuggest({

        data: magicData,
        //data: [{"id":"1", "name":"Paris"}, {"id":"2", "name":"New York"}],
        allowFreeEntries: false,
        valueField: 'id',
        displayField: 'name',
        allowDuplicates : false,
        expandOnFocus: true,
        required: true,
        noSuggestionText: 'No result matching  {{query}}',
        maxSuggestions: 5,

    });
}

function filterChange(filterSelect) {
    var TargetColumn = $(filterSelect).val();
    let rowID = $(filterSelect).parent().parent().attr("id").substring(10);
    console.log("Filter Changed for Row id : " + rowID);
    let filterConditionDOM = $(filterSelect).parent().parent().find(".filterCondition");
    let filterValueDOM = $(filterSelect).parent().parent().find(".filterValue");

    filterConditionDOM.empty().append('<option value="=">Equals</option><option value="!=">Not Equals</option>');

    filterValueDOM.empty().append('<div class="magicSuggest" name="magicSuggest"></div><b><small class="ErrorContainer">Error Message</small></b>');
    var magicData;
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({filter: TargetColumn}),
        dataType: 'json',
        url: '/getMagicSuggestData',
        async: false,
        success: function (data) {
            magicData = data;
        }
    });
    if (numericFilterArray.includes(TargetColumn)) {

        $.each(numericFilterOptions, function (optionText, optionValue) {
            filterConditionDOM.append(
                $('<option></option>').val(optionValue).html(optionText)
            );
        });
        filterValueDOM.find(".magicSuggest").append(numberInput);
    }
    else if (hugeFilterValueArray.includes(TargetColumn)){
        filterValueDOM.find(".magicSuggest").magicSuggest({
            // data: "/getData",
            // dataUrlParams: { filter: TargetColumn },
            allowFreeEntries: true,
            allowDuplicates : false,
            expandOnFocus: false,
            vtype: 'alphanum',
            maxDropHeight: 0,
        });
    }
    else{
        filterValueDOM.find(".magicSuggest").magicSuggest({
            data: magicData,
            valueField: 'id',
            displayField: 'name',
            allowFreeEntries: false,
            allowDuplicates : false,
            expandOnFocus: true,
            required: true,
            noSuggestionText: 'No result matching  {{query}}',
            maxSuggestions: 5,

        });
    }
}

// -----------------------------validation-----------------------------

function checkTitle(){
    let Title = $("#title")[0];
    if (Title.value.trim() === "") {
        onError(Title, "*Title cannot be empty");
        return false;

    } else if (Title.value.match(/[^A-Za-z 0-9]/g)) {
        onError(Title, "*Special Characters Are Not Allow");
        return false;
    } else {
        onSuccess(Title);
    }
}

function checkDescription(){
    let Description = $("#description")[0];
    if (Description.value.trim() === "") {
        onError(Description, "*Description cannot be empty");
        return false;
    } else {
        onSuccess(Description);
    }
}

function checkStartDateTime(){

    var startDate = $("#start_date")[0];
    var startTime = $("#start_time")[0];

    let valid = true;

    if( startTime.value != '' && startDate.value == ''){
        onError(startDate, "*Start Date required");
        valid = false;
    } else {
        onSuccess(startDate);
    }
    return valid;
}

function checkEndDateTime(){

    var endDate = $("#end_date")[0];
    var endTime = $("#end_time")[0];
    let valid = true;

    if( endTime.value != '' && endDate.value == ''){
        onError(endDate, "*Start Date required");
        valid = false;
    } else {
        onSuccess(endDate);
    }
    return valid;
}

function checkEmailTable(){
    let valid = true;

    $("#EmailTable tbody tr").each(function () {

        var email = $(this).find(".inputRecipient")[0];

        if (email.value.trim() === "") {
            onError(email, "*Recipient cannot be empty");
            valid = false;
        } else {
            onSuccess(email);
        }
    });

    return valid;
}

function checkFilterTable(){
    let valid = true;

    $("#FilterTable tbody tr").each(function () {

        if( $(this).find('input[name="magicSuggest[]"]').length == 0) {
            onError($(this).find(".filterValue")[0], "*Value cannot be empty");
            valid = false;
        } else {
            onSuccess($(this).find(".filterValue")[0]);
        }
    });

    return valid;
}

function validateInput() {

    var valid = true;

    vaild = checkTitle();
    valid = checkDescription() && valid;
    valid = checkStartDateTime() && valid;
    valid = checkEndDateTime() && valid;
    valid = checkEmailTable() && valid;
    valid = checkFilterTable() && valid;

    console.log("Validity", valid);

    return valid;
}

function onSuccess(input) {
    console.log("Success: ", input);
    $(input).parent().addClass("success");
    $(input).parent().removeClass("error");
    $(input).parent().find("small").css("visibility", "hidden");
}

function onError(input, message) {
    console.log("Error: ", input, message);
    console.log($(input).parent().find("b").html());
    $(input).parent().addClass("error");
    $(input).parent().removeClass("success");
    $(input).parent().find("small").text(message);
    $(input).parent().find("small").css("visibility", "visible");
    $(input).focus();
}

// -----------------------------submit-----------------------------
function submit() {


    var data = {
        "title": $("#title").val(),
        "description": $("#description").val(),
        "fields": selectedColumns.join(),
        "startDate": $("#start_date").val(),
        "startTime": $("#start_time").val(),
        "endDate": $("#end_date").val(),
        "endTime": $("#end_time").val(),
        "email": {},
        "filters": {}
    };

    let i = 0;
    $("#EmailTable tbody tr").each(function () {
        i = i + 1;
        data["email"][i] = {
            "recipient": $(this).find(".inputRecipient").val(),
            "frequency": $(this).find(".Frequency").val(),
        };
        let schedule = $(this).find(".time").val();
        if (data["email"][i]["frequency"] == "Monthly") {
            schedule += "," + $(this).find(".Dates").val();
        }
        else if (data["email"][i]["frequency"] == "Weekly") {
            schedule += "," + $(this).find(".SelectWeek").val();
        }
        data["email"][i]["schedule"] = schedule;
    });

    let j = 0;
    $("#FilterTable tbody tr").each(function () {
        j = j + 1

        let magicValues = []
        $(this).find('input[name="magicSuggest[]"]').each(function () {
            magicValues.push($(this).val());
        });

        data["filters"][j] = {
            "targetColumn": $(this).find(".filterColumn").val(),
            "condition": $(this).find(".filterCondition").val(),
            "value": magicValues.join(),
        };

    });

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/insertReport',

    }).done(function (data) {
        alert(data.message);
    })
}