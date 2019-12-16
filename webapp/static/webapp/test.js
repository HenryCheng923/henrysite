var numDiv=document.getElementsByName("db_data");//获取DIV
var num=numDiv.innerHTML;//获取DIV标签里的html
var col=Number(num)>"0"?"green":"red";
numDiv.style.color=col;


