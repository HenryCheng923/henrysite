var formattedDate = new Date("yourUnformattedOriginalDate");
var d = formattedDate.getDate();
var m =  formattedDate.getMonth();
m += 1;  // JavaScript months are 0-11
var y = formattedDate.getFullYear();

$("#txtDate").val(d + "." + m + "." + y);