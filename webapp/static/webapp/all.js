function ShowTime() {
    var NowDate = new Date();
    var Y = NowDate.getFullYear();
    var M = NowDate.getMonth()+1;
    var D = NowDate.getDate();
    var today =  Y + '-' + M + '-' + D;
    var startDate = document.querySelector("[name=start_date]");
    //var finishDate = document.querySelector("[name=finish_date]");
    var stock_price = document.querySelector("[name=stock_price]");
    startDate.value = today;
    //finishDate.value = today;
    stock_price.value = 30;
  }
