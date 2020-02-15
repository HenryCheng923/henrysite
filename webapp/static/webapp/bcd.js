alert("test");



var numDiv=document.querySelectorAll(".bbb td");//获取DIV
var num=numDiv.innerHTML;//获取DIV标签里的html
var col=Number(num)>"0"?"red":"red";
numDiv.style.color=col;
    