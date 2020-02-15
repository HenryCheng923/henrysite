from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from webapp.models import Company #呼叫webapp資料夾底下的models 的company函數，用來連結資料庫的方法
from webapp.models import All_sotck_daily_closing 
from webapp.models import Three_legal
from webapp.models import Three_legal_overbuysell
from webapp.models import All_stock_daily_closing
from webapp.models import Wespai_p49048
from webapp.models import Call_warrant
from django.db.models import Count
from django.db.models import Sum

from django.shortcuts import render_to_response
from django.shortcuts import redirect

from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import FloatField

import pandas
import time
import json
import datetime

import pymysql

insert_total = 0

today = datetime.datetime.today()

def pylinkweb(request):
	return HttpResponse("Django讓python能方便連結網頁")

def index(request):
    #now = datetime.now()
    return render(request,'index.html',locals())

def test(request):
    return render(request,'test.html',{})

#年金計算
def fv(request):
    return render(request,'E_10_1.html',{})
def result(request):
    pv=int(request.GET['amount'])
    i=float(request.GET['rate'])
    n=int(request.GET['period'])
    #d=int(request.POST['radio'])
    fv=str((pv*((1+i)**n)))
    
    #start_date = request.GET['start_date']
    return HttpResponse(fv)

#公司股票資料
def company(request):
    company = Company.objects.all()
    stockid = Company._meta.get_field('stockid').column
    abbreviation = Company._meta.get_field('abbreviation').column
    url = Company._meta.get_field('url').column
    industryname = Company._meta.get_field('industryname').column
    return render_to_response('company.html',locals())

def insert(request):
    	return render(request,'insert.html')

def do_insert(request):
    stockid = request.POST['stockid']
    abbreviation = request.POST['abbreviation']
    url = request.POST['url']
    employees = request.POST['employees']
    capital = request.POST['capital']
    industryname = request.POST['industryname']
    listeddate = request.POST['listeddate']
    Company.objects.create(stockid=stockid, abbreviation=abbreviation, url=url, employees=employees, capital=capital, industryname=industryname, listeddate=listeddate)
    return redirect('/company/')

def detail(request, stockid):
    detail = Company.objects.get(stockid=stockid)
    return render(request,'detail.html', {'detail': detail})

def update(request, stockid):
    update = Company.objects.get(stockid=stockid)
    return render(request,'update.html', {'update': update})


def do_update(request):
    stockid = request.POST['stockid']
    abbreviation = request.POST['abbreviation']
    url = request.POST['url']
    employees = request.POST['employees']
    capital = request.POST['capital']
    industryname = request.POST['industryname']
    listeddate = request.POST['listeddate']
    do_update = Company.objects.filter(stockid=stockid)
    do_update.update(abbreviation=abbreviation)
    do_update.update(url=url)
    do_update.update(employees=employees)
    do_update.update(capital=capital)
    do_update.update(industryname=industryname)
    do_update.update(listeddate=listeddate)
    return redirect('/company/')

def delete(request, stockid):
    delete = Company.objects.get(stockid=stockid)
    return render(request,'delete.html', {'delete': delete})


def do_delete(request):
    stockid = request.POST['stockid']	
    do_delete = Company.objects.filter(stockid=stockid)
    do_delete.delete()
    return redirect('/company/')

#股票每日資訊
def all_sotck_daily_closing(request):
    all_sotck_daily_closing = All_sotck_daily_closing.objects.all()
    st_date = All_sotck_daily_closing._meta.get_field('st_date').column
    st_stockno = All_sotck_daily_closing._meta.get_field('st_stockno').column
    st_stockname = All_sotck_daily_closing._meta.get_field('st_stockname').column
    return render_to_response('daily_if.html', locals())

#市場三大法人買賣金額統計表
def three_legal(request):
    #three_legal = Three_legal.objects.order_by("st_date")
    three_legal = Three_legal.objects.all().order_by("-st_date")[:10] #order_by 多一個"-"表示篩選出來的反過來排序
    return render_to_response('three_legal.html', locals())


    #
def E_14_2(request):
    return render(request,'E_14_2.html',{})

def E_14_2_Py(request):
    stock_id = request.GET['stock_id']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    response = E_14_2_main(stock_id, start_date, end_date)
    return HttpResponse(response)

#個股三大法人買賣超日報
def three_legal_overbuysell(request):
    	return render(request,'three_legal_overbuysell.html')

'''
def three_legal_overbuysell(request, stockno):
    getdata = Three_legal_overbuysell.objects.get(stockno = stockno)
    return render(request,'three_legal_overbuysell.html', {'getdata': getdata})

def do_search(request):
    #getvalue = Three_legal_overbuysell.objects.get(st_stockno=st_stockno)
    st_stockno_threelegal = request.GET['stockno']
    #getvalue = Three_legal_overbuysell.objects.filter(st_stockno=st_stockno)
    return render(request,'do_search.html',locals())
'''
def do_search(request):
    get_db_three_value_new = []
    if 'stockno' in request.GET:
        st_data = request.GET['stockno']
        get_db_three_value = Three_legal_overbuysell.objects.filter(Q(st_stockno__exact = st_data) |  Q(st_stockname__contains = st_data)).order_by("-st_date")
        return render(request,'do_search.html', locals())
    else:
        return redirect("/three_legal_overbuysell/")
    #stocknovalue = request.GET.get('st_stockno')
    #stocknovalue = request.GET['st_stockno']

def connect_mysql():  #連線資料庫 stockdatabase
    global connect, cursor
    connect = pymysql.connect(host = 'localhost', db = 'stockdatabase', user = 'root', password = 'b123456',
            charset = 'utf8', use_unicode = True)
    cursor = connect.cursor()

def connect_mysql_futuredatabase():  #連線資料庫 futuredatabase
    global connect, cursor
    connect = pymysql.connect(host = 'localhost', db = 'futuredatabase', user = 'root', password = 'b123456',
            charset = 'utf8', use_unicode = True)
    cursor = connect.cursor()

#投本比資料
def shareCapital_ratio(request):
    if 'start_date' in request.GET:
        date = request.GET.get('start_date')  # today.strftime("%Y%m%d")
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
        date = date_time.strftime('%Y%m%d')
    else:
        date = today.strftime("%Y%m%d")

    get_db_trust_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = date,  st_stockprice__gt = 30,  trust_stock_totalAmount__gt = 5000000, st_volume__gt = 1000, trust_buysell_shareCapital_ratio__gt = 0.1 ,foreign_buysell_shareCapital_ratio__gt = 0)\
                                                            .order_by("-trust_buysell_shareCapital_ratio")
    get_db_foreign_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = date,  st_stockprice__gt = 30,  foreign_stock_totalAmount__gt = 500000000, st_volume__gt = 1000, foreign_buysell_shareCapital_ratio__gt = 0.2, trust_buysell_shareCapital_ratio__gt = 0)\
                                                                        .order_by("-foreign_buysell_shareCapital_ratio")
    
    dealer_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = date,  st_stockprice__gt = 30,  dealer_stock_totalAmount__gt = 500000000, st_volume__gt = 1000, dealer_buysell_shareCapital_ratio__gt = 0.1, trust_buysell_shareCapital_ratio__gt = 0, foreign_buysell_shareCapital_ratio__gt = 0)\
                                                                        .order_by("-dealer_buysell_shareCapital_ratio")                                                                    
    #計算三日總和
    connect_mysql()
    three_date = "select st_date from stockdatabase.wespai_p49048  where st_stockno ='1101' order by st_date desc limit 0,3"
    cursor = connect.cursor()
    cursor.execute(three_date)  #執行查詢的SQL
    
    three_date_result = cursor.fetchall()  #如果有取出第一筆資料
    three_date_result = str(three_date_result[2][0].strftime("%Y%m%d")) #將日期轉換成YYYYMMDD
    print(three_date_result)
    get_db_trust_shareCapital_count = Wespai_p49048.objects.filter(st_date__range=[three_date_result, date],  st_stockprice__gt = 30,  foreign_stock_totalAmount__gt = 500000000, st_volume__gt = 1000)\
                                                            .values('st_stockno','st_stockname','industry_type')\
                                                            .annotate(trust_buysell_shareCapital_ratio = Cast(Sum('trust_buysell_shareCapital_ratio'), FloatField()))\
                                                            .order_by("-trust_buysell_shareCapital_ratio")

    '''
    from itertools import chain
    all_result = list(chain(get_db_trust_shareCapital_ratio, get_db_trust_shareCapital_count))
    print(get_db_trust_shareCapital_ratio)
    print(get_db_trust_shareCapital_count)
    print(type(all_result))
    '''
    #.annotate(trust_buysell_shareCapital_ratio = Cast(Sum('trust_buysell_shareCapital_ratio'), FloatField()))\

    #print(get_db_trust_shareCapital_count.values('st_stockname','trust_buysell_shareCapital_ratio'))                                                                                                                 
    #print(get_db_trust_shareCapital_count.st_stockno_count)
    '''
    #Transaction.objects.all().values('actor').annotate(total=Count('actor')).order_by('total')
    #c = Wespai_p49048.objects.annotate(Count(date))
    #
    '''
    
  
    
    #撈出近三日的所有資料，計算相同股票出現的投本比，然後用投本比由大至小排列
    return render_to_response('shareCapital_ratio.html', locals())



#認購權證總成交金額
def call_warrant(request):
    call_warrant_result = []
    if 'start_date' in request.GET:
        date = request.GET.get('start_date')  # today.strftime("%Y%m%d")
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
        date = date_time.strftime('%Y%m%d')
    else:
        date = today.strftime("%Y%m%d")
    
    connect_mysql()
    db_data = "select st_date,  st_stockname, st_close, sum(st_amount_call_warrant) as st_sum from stockdatabase.call_warrant where st_date = '%s' group by st_stockname having st_sum > 0 order by st_sum desc limit 0,30" % (date)
    cursor = connect.cursor()
    cursor.execute(db_data)  #執行查詢的SQL
    call_warrant_result = cursor.fetchall()  #如果有取出第一筆資料


    #計算三日總和

    connect_mysql()
    three_date = "select st_date from stockdatabase.call_warrant  where st_stockno_call_warrant ='034088' order by st_date desc limit 0,3"
    cursor = connect.cursor()
    cursor.execute(three_date)  #執行查詢的SQL
    
    three_date_result = cursor.fetchall()  #如果有取出第一筆資料
    three_date_result = str(three_date_result[2][0].strftime("%Y%m%d")) #將日期轉換成YYYYMMDD
    print(three_date_result)

    get_db_call_warrant_count = Call_warrant.objects.filter(st_date__range=[three_date_result, date])\
                                                        .values('st_stockno','st_stockname')\
                                                        .annotate(st_amount_call_warrant = Sum('st_amount_call_warrant'))\
                                                        .order_by("-st_amount_call_warrant")                                    
            
    return render_to_response('call_warrant.html', locals())




#外資比買超資料頁面
def foreign_buy_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        '''這是終止日期
        finish_date = request.POST.get('finish_date')
        date_time = datetime.datetime.strptime(finish_date,'%Y-%m-%d')
        finish_date = date_time.strftime('%Y%m%d')
        '''

        stock_price = request.POST.get('stock_price')
        foreign_stock_totalAmount = request.POST.get('foreign_stock_totalAmount')
        change_extent = request.POST.get('change_extent')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result
            
        #finish_date = 20191210
        stock_price = 30
        foreign_stock_totalAmount = 5000000
        change_extent = 3
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = 0.2

    get_db_foreign_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  foreign_stock_totalAmount__gte = foreign_stock_totalAmount, change_extent__lte = change_extent , st_volume__gte = st_volume, foreign_buysell_shareCapital_ratio__gte = foreign_shareCapital_ratio, trust_buysell_shareCapital_ratio__gt = trust_shareCapital_ratio)\
                                                                        .order_by("-foreign_buysell_shareCapital_ratio")

    return render_to_response('foreign_buy_shareCapital_ratio.html', locals())


#外資比賣超資料頁面
def foreign_sell_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        '''這是終止日期
        finish_date = request.POST.get('finish_date')
        date_time = datetime.datetime.strptime(finish_date,'%Y-%m-%d')
        finish_date = date_time.strftime('%Y%m%d')
        '''

        stock_price = request.POST.get('stock_price')
        foreign_stock_totalAmount = request.POST.get('foreign_stock_totalAmount')
        change_extent = request.POST.get('change_extent')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        #finish_date = 20191210
        stock_price = 30
        foreign_stock_totalAmount = 5000000
        change_extent = -3
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = -0.2

    get_db_foreign_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  foreign_stock_totalAmount__gte = foreign_stock_totalAmount, change_extent__gte = change_extent ,st_volume__gte = st_volume, foreign_buysell_shareCapital_ratio__lte = foreign_shareCapital_ratio, trust_buysell_shareCapital_ratio__lt = trust_shareCapital_ratio)\
                                                                        .order_by("foreign_buysell_shareCapital_ratio")

    return render_to_response('foreign_sell_shareCapital_ratio.html', locals())


#投信比買超資料頁面
def trust_buy_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        '''這是終止日期
        finish_date = request.POST.get('finish_date')
        date_time = datetime.datetime.strptime(finish_date,'%Y-%m-%d')
        finish_date = date_time.strftime('%Y%m%d')
        '''

        stock_price = request.POST.get('stock_price')
        trust_stock_totalAmount = request.POST.get('trust_stock_totalAmount')
        change_extent = request.POST.get('change_extent')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        #finish_date = 20191210
        stock_price = 30
        trust_stock_totalAmount = 5000000
        change_extent = 3
        st_volume = 1000
        trust_shareCapital_ratio = 0.1
        foreign_shareCapital_ratio = 0

    get_db_trust_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  trust_stock_totalAmount__gte = trust_stock_totalAmount, change_extent__lte = change_extent, st_volume__gte = st_volume, trust_buysell_shareCapital_ratio__gte = trust_shareCapital_ratio ,foreign_buysell_shareCapital_ratio__gt = foreign_shareCapital_ratio)\
                                                            .order_by("-trust_buysell_shareCapital_ratio")

    return render_to_response('trust_buy_shareCapital_ratio.html', locals())


#投信比賣超資料頁面
def trust_sell_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        '''這是終止日期
        finish_date = request.POST.get('finish_date')
        date_time = datetime.datetime.strptime(finish_date,'%Y-%m-%d')
        finish_date = date_time.strftime('%Y%m%d')
        '''

        stock_price = request.POST.get('stock_price')
        trust_stock_totalAmount = request.POST.get('trust_stock_totalAmount')
        change_extent = request.POST.get('change_extent')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result
        
        #finish_date = 20191210
        stock_price = 30
        trust_stock_totalAmount = 5000000
        change_extent = -3
        st_volume = 1000
        trust_shareCapital_ratio = -0.1
        foreign_shareCapital_ratio = 0

    get_db_trust_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  trust_stock_totalAmount__gte = trust_stock_totalAmount, change_extent__gte = change_extent, st_volume__gte = st_volume, trust_buysell_shareCapital_ratio__lte = trust_shareCapital_ratio ,foreign_buysell_shareCapital_ratio__lt = foreign_shareCapital_ratio)\
                                                            .order_by("trust_buysell_shareCapital_ratio")

    return render_to_response('trust_sell_shareCapital_ratio.html', locals())

#自營比買超資料頁面
def dealer_buy_shareCapital_ratio(request):
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        '''這是終止日期
        finish_date = request.POST.get('finish_date')
        date_time = datetime.datetime.strptime(finish_date,'%Y-%m-%d')
        finish_date = date_time.strftime('%Y%m%d')
        '''

        stock_price = request.POST.get('stock_price')
        trust_stock_totalAmount = request.POST.get('trust_stock_totalAmount')
        change_extent = request.POST.get('change_extent')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
        dealer_shareCapital_ratio = request.POST.get('dealer_shareCapital_ratio')
    else:
        start_date = date
        #finish_date = 20191210
        stock_price = 30
        trust_stock_totalAmount = 5000000
        change_extent = 3
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = 0
        dealer_shareCapital_ratio = 0.1

    get_db_dealer_buy_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  dealer_stock_totalAmount__gt = trust_stock_totalAmount, change_extent__lte = change_extent, st_volume__gte = st_volume,  trust_buysell_shareCapital_ratio__gte = trust_shareCapital_ratio, foreign_buysell_shareCapital_ratio__gte = foreign_shareCapital_ratio, dealer_buysell_shareCapital_ratio__gte = dealer_shareCapital_ratio)\
                                                               .order_by("-dealer_buysell_shareCapital_ratio")                                                                    
   

    return render_to_response('dealer_buy_shareCapital_ratio.html', locals())



#自營比賣超資料頁面
def dealer_sell_shareCapital_ratio(request):
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        '''這是終止日期
        finish_date = request.POST.get('finish_date')
        date_time = datetime.datetime.strptime(finish_date,'%Y-%m-%d')
        finish_date = date_time.strftime('%Y%m%d')
        '''

        stock_price = request.POST.get('stock_price')
        trust_stock_totalAmount = request.POST.get('trust_stock_totalAmount')
        change_extent = request.POST.get('change_extent')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
        dealer_shareCapital_ratio = request.POST.get('dealer_shareCapital_ratio')
    else:
        start_date = date
        #finish_date = 20191210
        stock_price = 30
        trust_stock_totalAmount = 5000000
        change_extent = 3
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = 0
        dealer_shareCapital_ratio = -0.1

    get_db_dealer_sell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  dealer_stock_totalAmount__gt = trust_stock_totalAmount, change_extent__gte = change_extent, st_volume__gte = st_volume,  trust_buysell_shareCapital_ratio__gte = trust_shareCapital_ratio, foreign_buysell_shareCapital_ratio__gte = foreign_shareCapital_ratio, dealer_buysell_shareCapital_ratio__lte = dealer_shareCapital_ratio)\
                                                               .order_by("dealer_buysell_shareCapital_ratio")                                                                    
   

    return render_to_response('dealer_sell_shareCapital_ratio.html', locals())

import program.getdata as Gt

#外資比買超累計資料頁面
def foreign_buyAcc_shareCapital_ratio(request):
    '''
    connect_mysql()
    getdb_st_date = "select st_date from stockdatabase.wespai_p49048 where st_stockno = 1101 order by st_date desc"
    cursor2 = connect.cursor()
    cursor2.execute(getdb_st_date)  #執行查詢的SQL
    getdb_st_date = cursor2.fetchone()  #如果有取出第一筆資料
    getdb_st_date_result = getdb_st_date[0].strftime('%Y%m%d')
    '''
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        foreign_ratio_day1 = request.POST.get('foreign_ratio_day1')
        foreign_ratio_day3 = request.POST.get('foreign_ratio_day3')
        foreign_ratio_day5 = request.POST.get('foreign_ratio_day5')
        foreign_ratio_day10 = request.POST.get('foreign_ratio_day10')
        foreign_turnover_day1 = request.POST.get('foreign_turnover_day1')
        foreign_turnover_day3 = request.POST.get('foreign_turnover_day3')
        foreign_turnover_day5 = request.POST.get('foreign_turnover_day5')
        foreign_turnover_day10 = request.POST.get('foreign_turnover_day10')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        stock_price = 30
        change_extent = 3
        foreign_ratio_day1 = 0.1
        foreign_ratio_day3 = 0
        foreign_ratio_day5 = 0
        foreign_ratio_day10 = 0
        foreign_turnover_day1 = 0
        foreign_turnover_day3 = 0
        foreign_turnover_day5 = 0
        foreign_turnover_day10 = 0

    
    foreignDay = \
    "select *, convert(st_volume/issued_number,decimal(15,2)) as turnover1 \
    from stockdatabase.wespai_p49048 A join ( select B.st_stockno, sum(foreign_buysell_shareCapital_ratio) as sum_foreign3, convert((sum(st_volume)/issued_number)/3,decimal(15,2)) as turnover3 \
    from stockdatabase.wespai_p49048 B \
    where b.st_date between DATE_SUB('%s',INTERVAL 2 DAY) and  '%s'  \
    group by B.st_stockno \
    ) B join ( \
    select c.st_stockno, sum(foreign_buysell_shareCapital_ratio) as sum_foreign5, convert((sum(st_volume)/issued_number)/5,decimal(15,2)) as turnover5 \
    from stockdatabase.wespai_p49048 c \
    where c.st_date between DATE_SUB('%s',INTERVAL 4 DAY) and  '%s'  \
    group by c.st_stockno \
    ) C join ( \
    select d.st_stockno, sum(foreign_buysell_shareCapital_ratio) as sum_foreign10, convert((sum(st_volume)/issued_number)/10,decimal(15,2)) as turnover10 \
    from stockdatabase.wespai_p49048 d \
    where d.st_date between DATE_SUB('%s',INTERVAL 9 DAY) and  '%s'  \
    group by d.st_stockno \
    ) D on A.st_stockno = B.st_stockno and A.st_stockno = C.st_stockno and A.st_stockno = D.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice > '%s' and change_extent <= '%s' and foreign_buysell_shareCapital_ratio >'%s' and sum_foreign3 > '%s' and sum_foreign5 > '%s' and sum_foreign10 > '%s' and turnover1 > '%s' and  turnover3 > '%s' and turnover5 > '%s' and turnover10 > '%s' order by turnover1 desc" \
    % (start_date,start_date,start_date,start_date,start_date,start_date,start_date,stock_price,change_extent ,foreign_ratio_day1 ,foreign_ratio_day3,foreign_ratio_day5,foreign_ratio_day10,foreign_turnover_day1,foreign_turnover_day3,foreign_turnover_day5,foreign_turnover_day10)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(foreignDay)  #執行查詢的SQL
    foreignDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('foreign_buyAcc_shareCapital_ratio.html', locals())



#投信比買超累計資料頁面
def trust_buyAcc_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        trust_ratio_day1 = request.POST.get('trust_ratio_day1')
        trust_ratio_day3 = request.POST.get('trust_ratio_day3')
        trust_ratio_day5 = request.POST.get('trust_ratio_day5')
        trust_ratio_day10 = request.POST.get('trust_ratio_day10')
        trust_turnover_day1 = request.POST.get('trust_turnover_day1')
        trust_turnover_day3 = request.POST.get('trust_turnover_day3')
        trust_turnover_day5 = request.POST.get('trust_turnover_day5')
        trust_turnover_day10 = request.POST.get('trust_turnover_day10')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        stock_price = 30
        change_extent = 3
        trust_ratio_day1 = 0.1
        trust_ratio_day3 = 0
        trust_ratio_day5 = 0
        trust_ratio_day10 = 0
        trust_turnover_day1 = 0
        trust_turnover_day3 = 0
        trust_turnover_day5 = 0
        trust_turnover_day10 = 0

    
    trustDay = \
    "select *, convert(st_volume/issued_number,decimal(15,2)) as turnover1 \
    from stockdatabase.wespai_p49048 A join ( select B.st_stockno, sum(trust_buysell_shareCapital_ratio) as sum_trust3, convert((sum(st_volume)/issued_number)/3,decimal(15,2)) as turnover3 \
    from stockdatabase.wespai_p49048 B \
    where b.st_date between DATE_SUB('%s',INTERVAL 2 DAY) and  '%s'  \
    group by B.st_stockno \
    ) B join ( \
    select c.st_stockno, sum(trust_buysell_shareCapital_ratio) as sum_trust5, convert((sum(st_volume)/issued_number)/5,decimal(15,2)) as turnover5 \
    from stockdatabase.wespai_p49048 c \
    where c.st_date between DATE_SUB('%s',INTERVAL 4 DAY) and  '%s'  \
    group by c.st_stockno \
    ) C join ( \
    select d.st_stockno, sum(trust_buysell_shareCapital_ratio) as sum_trust10, convert((sum(st_volume)/issued_number)/10,decimal(15,2)) as turnover10 \
    from stockdatabase.wespai_p49048 d \
    where d.st_date between DATE_SUB('%s',INTERVAL 9 DAY) and  '%s'  \
    group by d.st_stockno \
    ) D on A.st_stockno = B.st_stockno and A.st_stockno = C.st_stockno and A.st_stockno = D.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice > '%s' and change_extent <= '%s' and trust_buysell_shareCapital_ratio >'%s' and sum_trust3 > '%s' and sum_trust5 > '%s' and sum_trust10 > '%s' and turnover1 > '%s' and  turnover3 > '%s' and turnover5 > '%s' and turnover10 > '%s' order by turnover1 desc" \
    % (start_date,start_date,start_date,start_date,start_date,start_date,start_date,stock_price, change_extent, trust_ratio_day1 ,trust_ratio_day3,trust_ratio_day5,trust_ratio_day10,trust_turnover_day1,trust_turnover_day3,trust_turnover_day5,trust_turnover_day10)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(trustDay)  #執行查詢的SQL
    trustDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('trust_buyAcc_shareCapital_ratio.html', locals())


#自營比買超累計資料頁面
def dealer_buyAcc_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        dealer_ratio_day1 = request.POST.get('dealer_ratio_day1')
        dealer_ratio_day3 = request.POST.get('dealer_ratio_day3')
        dealer_ratio_day5 = request.POST.get('dealer_ratio_day5')
        dealer_ratio_day10 = request.POST.get('dealer_ratio_day10')
        dealer_turnover_day1 = request.POST.get('dealer_turnover_day1')
        dealer_turnover_day3 = request.POST.get('dealer_turnover_day3')
        dealer_turnover_day5 = request.POST.get('dealer_turnover_day5')
        dealer_turnover_day10 = request.POST.get('dealer_turnover_day10')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        stock_price = 30
        change_extent = 3
        dealer_ratio_day1 = 0.1
        dealer_ratio_day3 = 0
        dealer_ratio_day5 = 0
        dealer_ratio_day10 = 0
        dealer_turnover_day1 = 0
        dealer_turnover_day3 = 0
        dealer_turnover_day5 = 0
        dealer_turnover_day10 = 0

    
    dealerDay = \
    "select *, convert(st_volume/issued_number,decimal(15,2)) as turnover1 \
    from stockdatabase.wespai_p49048 A join ( select B.st_stockno, sum(dealer_buysell_shareCapital_ratio) as sum_dealer3, convert((sum(st_volume)/issued_number)/3,decimal(15,2)) as turnover3 \
    from stockdatabase.wespai_p49048 B \
    where b.st_date between DATE_SUB('%s',INTERVAL 2 DAY) and  '%s'  \
    group by B.st_stockno \
    ) B join ( \
    select c.st_stockno, sum(dealer_buysell_shareCapital_ratio) as sum_dealer5, convert((sum(st_volume)/issued_number)/5,decimal(15,2)) as turnover5 \
    from stockdatabase.wespai_p49048 c \
    where c.st_date between DATE_SUB('%s',INTERVAL 4 DAY) and  '%s'  \
    group by c.st_stockno \
    ) C join ( \
    select d.st_stockno, sum(dealer_buysell_shareCapital_ratio) as sum_dealer10, convert((sum(st_volume)/issued_number)/10,decimal(15,2)) as turnover10 \
    from stockdatabase.wespai_p49048 d \
    where d.st_date between DATE_SUB('%s',INTERVAL 9 DAY) and  '%s'  \
    group by d.st_stockno \
    ) D on A.st_stockno = B.st_stockno and A.st_stockno = C.st_stockno and A.st_stockno = D.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice > '%s' and change_extent <= '%s' and dealer_buysell_shareCapital_ratio >'%s' and sum_dealer3 > '%s' and sum_dealer5 > '%s' and sum_dealer10 > '%s' and turnover1 > '%s' and  turnover3 > '%s' and turnover5 > '%s' and turnover10 > '%s' order by turnover1 desc" \
    % (start_date,start_date,start_date,start_date,start_date,start_date,start_date,stock_price, change_extent, dealer_ratio_day1 ,dealer_ratio_day3,dealer_ratio_day5,dealer_ratio_day10,dealer_turnover_day1,dealer_turnover_day3,dealer_turnover_day5,dealer_turnover_day10)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(dealerDay)  #執行查詢的SQL
    dealerDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('dealer_buyAcc_shareCapital_ratio.html', locals())


#外資比賣超累計資料頁面
def foreign_sellAcc_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        foreign_ratio_day1 = request.POST.get('foreign_ratio_day1')
        foreign_ratio_day3 = request.POST.get('foreign_ratio_day3')
        foreign_ratio_day5 = request.POST.get('foreign_ratio_day5')
        foreign_ratio_day10 = request.POST.get('foreign_ratio_day10')
        foreign_turnover_day1 = request.POST.get('foreign_turnover_day1')
        foreign_turnover_day3 = request.POST.get('foreign_turnover_day3')
        foreign_turnover_day5 = request.POST.get('foreign_turnover_day5')
        foreign_turnover_day10 = request.POST.get('foreign_turnover_day10')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        stock_price = 30
        change_extent = -3
        foreign_ratio_day1 = -0.1
        foreign_ratio_day3 = 0
        foreign_ratio_day5 = 0
        foreign_ratio_day10 = 0
        foreign_turnover_day1 = 0
        foreign_turnover_day3 = 0
        foreign_turnover_day5 = 0
        foreign_turnover_day10 = 0

    
    foreignDay = \
    "select *, convert(st_volume/issued_number,decimal(15,2)) as turnover1 \
    from stockdatabase.wespai_p49048 A join ( select B.st_stockno, sum(foreign_buysell_shareCapital_ratio) as sum_foreign3, convert((sum(st_volume)/issued_number)/3,decimal(15,2)) as turnover3 \
    from stockdatabase.wespai_p49048 B \
    where b.st_date between DATE_SUB('%s',INTERVAL 2 DAY) and  '%s'  \
    group by B.st_stockno \
    ) B join ( \
    select c.st_stockno, sum(foreign_buysell_shareCapital_ratio) as sum_foreign5, convert((sum(st_volume)/issued_number)/5,decimal(15,2)) as turnover5 \
    from stockdatabase.wespai_p49048 c \
    where c.st_date between DATE_SUB('%s',INTERVAL 4 DAY) and  '%s'  \
    group by c.st_stockno \
    ) C join ( \
    select d.st_stockno, sum(foreign_buysell_shareCapital_ratio) as sum_foreign10, convert((sum(st_volume)/issued_number)/10,decimal(15,2)) as turnover10 \
    from stockdatabase.wespai_p49048 d \
    where d.st_date between DATE_SUB('%s',INTERVAL 9 DAY) and  '%s'  \
    group by d.st_stockno \
    ) D on A.st_stockno = B.st_stockno and A.st_stockno = C.st_stockno and A.st_stockno = D.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice > '%s' and change_extent >= '%s' and foreign_buysell_shareCapital_ratio < '%s' and sum_foreign3 < '%s' and sum_foreign5 < '%s' and sum_foreign10 < '%s' and turnover1 > '%s' and  turnover3 > '%s' and turnover5 > '%s' and turnover10 > '%s' order by turnover1 desc" \
    % (start_date,start_date,start_date,start_date,start_date,start_date,start_date,stock_price,change_extent ,foreign_ratio_day1 ,foreign_ratio_day3,foreign_ratio_day5,foreign_ratio_day10,foreign_turnover_day1,foreign_turnover_day3,foreign_turnover_day5,foreign_turnover_day10)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(foreignDay)  #執行查詢的SQL
    foreignDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('foreign_sellAcc_shareCapital_ratio.html', locals())

#投信比賣超累計資料頁面
def trust_sellAcc_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        trust_ratio_day1 = request.POST.get('trust_ratio_day1')
        trust_ratio_day3 = request.POST.get('trust_ratio_day3')
        trust_ratio_day5 = request.POST.get('trust_ratio_day5')
        trust_ratio_day10 = request.POST.get('trust_ratio_day10')
        trust_turnover_day1 = request.POST.get('trust_turnover_day1')
        trust_turnover_day3 = request.POST.get('trust_turnover_day3')
        trust_turnover_day5 = request.POST.get('trust_turnover_day5')
        trust_turnover_day10 = request.POST.get('trust_turnover_day10')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        stock_price = 30
        change_extent = -3
        trust_ratio_day1 = -0.1
        trust_ratio_day3 = 0
        trust_ratio_day5 = 0
        trust_ratio_day10 = 0
        trust_turnover_day1 = 0
        trust_turnover_day3 = 0
        trust_turnover_day5 = 0
        trust_turnover_day10 = 0

    
    trustDay = \
    "select *, convert(st_volume/issued_number,decimal(15,2)) as turnover1 \
    from stockdatabase.wespai_p49048 A join ( select B.st_stockno, sum(trust_buysell_shareCapital_ratio) as sum_trust3, convert((sum(st_volume)/issued_number)/3,decimal(15,2)) as turnover3 \
    from stockdatabase.wespai_p49048 B \
    where b.st_date between DATE_SUB('%s',INTERVAL 2 DAY) and  '%s'  \
    group by B.st_stockno \
    ) B join ( \
    select c.st_stockno, sum(trust_buysell_shareCapital_ratio) as sum_trust5, convert((sum(st_volume)/issued_number)/5,decimal(15,2)) as turnover5 \
    from stockdatabase.wespai_p49048 c \
    where c.st_date between DATE_SUB('%s',INTERVAL 4 DAY) and  '%s'  \
    group by c.st_stockno \
    ) C join ( \
    select d.st_stockno, sum(trust_buysell_shareCapital_ratio) as sum_trust10, convert((sum(st_volume)/issued_number)/10,decimal(15,2)) as turnover10 \
    from stockdatabase.wespai_p49048 d \
    where d.st_date between DATE_SUB('%s',INTERVAL 9 DAY) and  '%s'  \
    group by d.st_stockno \
    ) D on A.st_stockno = B.st_stockno and A.st_stockno = C.st_stockno and A.st_stockno = D.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice > '%s' and change_extent >= '%s' and trust_buysell_shareCapital_ratio <'%s' and sum_trust3 < '%s' and sum_trust5 < '%s' and sum_trust10 < '%s' and turnover1 > '%s' and  turnover3 > '%s' and turnover5 > '%s' and turnover10 > '%s' order by turnover1 desc" \
    % (start_date,start_date,start_date,start_date,start_date,start_date,start_date,stock_price, change_extent, trust_ratio_day1 ,trust_ratio_day3,trust_ratio_day5,trust_ratio_day10,trust_turnover_day1,trust_turnover_day3,trust_turnover_day5,trust_turnover_day10)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(trustDay)  #執行查詢的SQL
    trustDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('trust_sellAcc_shareCapital_ratio.html', locals())



#自營比賣超累計資料頁面
def dealer_sellAcc_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        dealer_ratio_day1 = request.POST.get('dealer_ratio_day1')
        dealer_ratio_day3 = request.POST.get('dealer_ratio_day3')
        dealer_ratio_day5 = request.POST.get('dealer_ratio_day5')
        dealer_ratio_day10 = request.POST.get('dealer_ratio_day10')
        dealer_turnover_day1 = request.POST.get('dealer_turnover_day1')
        dealer_turnover_day3 = request.POST.get('dealer_turnover_day3')
        dealer_turnover_day5 = request.POST.get('dealer_turnover_day5')
        dealer_turnover_day10 = request.POST.get('dealer_turnover_day10')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result

        stock_price = 30
        change_extent = -3
        dealer_ratio_day1 = -0.1
        dealer_ratio_day3 = 0
        dealer_ratio_day5 = 0
        dealer_ratio_day10 = 0
        dealer_turnover_day1 = 0
        dealer_turnover_day3 = 0
        dealer_turnover_day5 = 0
        dealer_turnover_day10 = 0

    
    dealerDay = \
    "select *, convert(st_volume/issued_number,decimal(15,2)) as turnover1 \
    from stockdatabase.wespai_p49048 A join ( select B.st_stockno, sum(dealer_buysell_shareCapital_ratio) as sum_dealer3, convert((sum(st_volume)/issued_number)/3,decimal(15,2)) as turnover3 \
    from stockdatabase.wespai_p49048 B \
    where b.st_date between DATE_SUB('%s',INTERVAL 2 DAY) and  '%s'  \
    group by B.st_stockno \
    ) B join ( \
    select c.st_stockno, sum(dealer_buysell_shareCapital_ratio) as sum_dealer5, convert((sum(st_volume)/issued_number)/5,decimal(15,2)) as turnover5 \
    from stockdatabase.wespai_p49048 c \
    where c.st_date between DATE_SUB('%s',INTERVAL 4 DAY) and  '%s'  \
    group by c.st_stockno \
    ) C join ( \
    select d.st_stockno, sum(dealer_buysell_shareCapital_ratio) as sum_dealer10, convert((sum(st_volume)/issued_number)/10,decimal(15,2)) as turnover10 \
    from stockdatabase.wespai_p49048 d \
    where d.st_date between DATE_SUB('%s',INTERVAL 9 DAY) and  '%s'  \
    group by d.st_stockno \
    ) D on A.st_stockno = B.st_stockno and A.st_stockno = C.st_stockno and A.st_stockno = D.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice > '%s' and change_extent >= '%s' and dealer_buysell_shareCapital_ratio <'%s' and sum_dealer3 < '%s' and sum_dealer5 < '%s' and sum_dealer10 < '%s' and turnover1 > '%s' and  turnover3 > '%s' and turnover5 > '%s' and turnover10 > '%s' order by turnover1 desc" \
    % (start_date,start_date,start_date,start_date,start_date,start_date,start_date,stock_price, change_extent, dealer_ratio_day1 ,dealer_ratio_day3,dealer_ratio_day5,dealer_ratio_day10,dealer_turnover_day1,dealer_turnover_day3,dealer_turnover_day5,dealer_turnover_day10)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(dealerDay)  #執行查詢的SQL
    dealerDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('dealer_sellAcc_shareCapital_ratio.html', locals())


#認購權證比資料頁面
def call_warrant_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        call_warrant_shareCapital_ratio = request.POST.get('call_warrant_shareCapital_ratio')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result
            
        stock_price = 30
        change_extent = 3
        call_warrant_shareCapital_ratio = 0.5

    dealerDay = \
    "select *, convert(st_sum/A.issued_number,decimal(15,3)) as call_warrant_radio \
    from stockdatabase.wespai_p49048 A join ( select B.st_date,B.st_stockno,  B.st_stockname, B.st_close, (sum(st_amount_call_warrant)/B.st_close) as st_sum \
    from stockdatabase.call_warrant as B \
	where B.st_date = '%s' \
    group by B.st_stockname \
    ) B  on A.st_stockno = B.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice >= '%s' and change_extent <= '%s' and call_warrant_radio  > '%s' order by call_warrant_radio desc " \
    % (start_date, start_date, stock_price, change_extent, call_warrant_shareCapital_ratio)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(dealerDay)  #執行查詢的SQL
    call_warrantDay_result = cursor.fetchall()  #如果有取出第一筆資料
    return render_to_response('warrant/call_warrant_shareCapital_ratio.html', locals())


#認售權證比資料頁面
def put_warrant_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        change_extent = request.POST.get('change_extent')
        put_warrant_shareCapital_ratio = request.POST.get('put_warrant_shareCapital_ratio')
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result
            
        stock_price = 30
        change_extent = 3
        put_warrant_shareCapital_ratio = 0.1

    dealerDay = \
    "select *, convert(st_sum/A.issued_number,decimal(15,3)) as put_warrant_radio \
    from stockdatabase.wespai_p49048 A join ( select B.st_date,B.st_stockno,  B.st_stockname, B.st_close, (sum(st_amount_put_warrant)/B.st_close) as st_sum \
    from stockdatabase.put_warrant as B \
	where B.st_date = '%s' \
    group by B.st_stockname \
    ) B  on A.st_stockno = B.st_stockno \
    where A.st_date = '%s' \
    having st_stockprice >= '%s' and change_extent <= '%s' and put_warrant_radio > '%s' order by put_warrant_radio desc " \
    % (start_date, start_date, stock_price, change_extent, put_warrant_shareCapital_ratio)

    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(dealerDay)  #執行查詢的SQL
    put_warrantDay_result = cursor.fetchall()  #如果有取出第一筆資料
    return render_to_response('warrant/put_warrant_shareCapital_ratio.html', locals())


#任我行籌碼分析表
def chip_analysis(request):
    '''
    connect_mysql()
    getdb_st_date = "select st_date from stockdatabase.wespai_p49048 where st_stockno = 1101 order by st_date desc"
    cursor2 = connect.cursor()
    cursor2.execute(getdb_st_date)  #執行查詢的SQL
    getdb_st_date = cursor2.fetchone()  #如果有取出第一筆資料
    getdb_st_date_result = getdb_st_date[0].strftime('%Y%m%d')
    '''
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    
    chip_analysis = \
    "select * \
    from stockdatabase.three_legal as A join ( \
	select * \
    from stockdatabase.credit_transaction as B \
    ) B join ( \
	select * \
    from stockdatabase.market_transaction_information as C \
    ) C on A.st_date = B.st_date and A.st_date = C.st_date order by A.st_date desc limit 0,30" \
    
    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(chip_analysis)  #執行查詢的SQL
    chip_analysis_result = cursor.fetchall()  #如果有取出第一筆資料
    return render_to_response('chip_analysis.html', locals())

#三大法人買超比資料頁面
def three_buy_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        amount_of_capital = request.POST.get('amount_of_capital')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
        dealer_shareCapital_ratio = request.POST.get('dealer_shareCapital_ratio')
        three_shareCapital_ratio = request.POST.get('three_shareCapital_ratio')
        
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result
            
        
        stock_price = 30
        amount_of_capital = 100
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = 0
        dealer_shareCapital_ratio = 0
        three_shareCapital_ratio = 0

    trustDay = \
    "select st_date, st_stockno, st_stockname, st_stockprice, amount_of_capital, industry_type, convert(foreign_buysell/st_volume,decimal(15,2)) as foreign_volume, convert(trust_buysell/st_volume,decimal(15,2)) as trust_volume	,convert(dealer_buysell/st_volume,decimal(15,2)) as dealer_volume, convert(st_three_buysell/st_volume,decimal(15,2)) as st_three_volume, st_volume \
    from stockdatabase.wespai_p49048 \
    where st_date between '%s' and  '%s'  and amount_of_capital < '%s' and st_volume >'%s' \
    having foreign_volume > '%s'  and trust_volume > '%s' and dealer_volume > '%s' and st_three_volume > '%s' \
    order by st_three_volume desc" \
    %(start_date,start_date,amount_of_capital,st_volume,trust_shareCapital_ratio,foreign_shareCapital_ratio,dealer_shareCapital_ratio,three_shareCapital_ratio)


    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(trustDay)  #執行查詢的SQL
    trustDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('three_buy_shareCapital_ratio.html', locals())


#三大法人賣超比資料頁面
def three_sell_shareCapital_ratio(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    if request.POST:
        start_date = request.POST.get('start_date')
        date_time = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        start_date = date_time.strftime('%Y%m%d')

        stock_price = request.POST.get('stock_price')
        amount_of_capital = request.POST.get('amount_of_capital')
        st_volume = request.POST.get('st_volume')
        trust_shareCapital_ratio = request.POST.get('trust_shareCapital_ratio')
        foreign_shareCapital_ratio = request.POST.get('foreign_shareCapital_ratio')
        dealer_shareCapital_ratio = request.POST.get('dealer_shareCapital_ratio')
        three_shareCapital_ratio = request.POST.get('three_shareCapital_ratio')
        
    else:
        if getdb_st_date_result == date:
            start_date = date
        else:
            start_date = getdb_st_date_result
            
        
        stock_price = 30
        amount_of_capital = 100
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = 0
        dealer_shareCapital_ratio = 0
        three_shareCapital_ratio = 0

    trustDay = \
    "select st_date, st_stockno, st_stockname, st_stockprice, amount_of_capital, industry_type, convert(foreign_buysell/st_volume,decimal(15,2)) as foreign_volume, convert(trust_buysell/st_volume,decimal(15,2)) as trust_volume	,convert(dealer_buysell/st_volume,decimal(15,2)) as dealer_volume, convert(st_three_buysell/st_volume,decimal(15,2)) as st_three_volume, st_volume \
    from stockdatabase.wespai_p49048 \
    where st_date between '%s' and  '%s'  and amount_of_capital < '%s' and st_volume >'%s' \
    having foreign_volume < '%s'  and trust_volume < '%s' and dealer_volume < '%s' and st_three_volume < '%s' \
    order by st_three_volume" \
    %(start_date,start_date,amount_of_capital,st_volume,trust_shareCapital_ratio,foreign_shareCapital_ratio,dealer_shareCapital_ratio,three_shareCapital_ratio)


    connect_mysql()
    cursor = connect.cursor()
    cursor.execute(trustDay)  #執行查詢的SQL
    trustDay_result = cursor.fetchall()  #如果有取出第一筆資料

    return render_to_response('three_sell_shareCapital_ratio.html', locals())


#任我行籌碼分析表
def futures_chips(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")
    
    chip_analysis = \
    "select st_date, s_close, s_updown,s_updown_radio,s_callput_diff,s_callput_amount_radio,s_BS_amount_radio,retail_BS_ratio,top_B_five_traders_diff,top_B_five_specificlegal_diff,top_B_ten_traders_diff,top_B_ten_specificlegal_diff \
    from futuredatabase.futures_three_legal \
    order by st_date desc limit 0,30" \
    
    connect_mysql_futuredatabase()
    cursor = connect.cursor()
    cursor.execute(chip_analysis)  #執行查詢的SQL
    chip_analysis_result = cursor.fetchall()  #如果有取出第一筆資料
    return render_to_response('futures_chips.html', locals())


#任我行籌碼分析表
def internationIndex(request):
    getdb_st_date_result = Gt.getdata()
    date = today.strftime("%Y%m%d")

    dfs = pandas.read_html("https://histock.tw/%E5%9C%8B%E9%9A%9B%E8%82%A1%E5%B8%82")
    item0  = dfs[0] #費城半導體~俄羅斯
    item1  = dfs[1] #小日經~以太幣
    item2  = dfs[2] #日本日經~台S&P500
    item3  = dfs[3] #臺道瓊~加拿大
    item4  = dfs[4] #小德國~奈及利亞
    item5  = dfs[5] #深證100指數~巴基斯坦
    item6  = dfs[6] #奧地利~瑞士
    item7  = dfs[7] #澳大利亞~美國
    item8  = dfs[8] #孟加拉~越南
    item9  = dfs[9] #台積電ADR~和信GIGA
    item10  = dfs[10] #高股息~中型100
    item11  = dfs[11] #台指期~摩台指
    item12  = dfs[12] #比特幣~NEO
    item13  = dfs[13] #乾散裝~超輕便
    item14  = dfs[14] #汽油~天燃氣
    item15  = dfs[15] #泰德價差~VIX
    item16  = dfs[16] #歐元兌美元~加幣
    item17  = dfs[17] #人民幣~馬來幣
    item18  = dfs[18] #AC世界指數~台灣指數
    item19  = dfs[19] #肉牛~11號糖
    item20  = dfs[20] #白金~鋅

    #亞太區追蹤
    AsiaIndex =  [
            [item2.iloc[0,0],item2.iloc[0,1],item2.iloc[0,2],item2.iloc[0,3],item3.iloc[0,4]], #日本日經
            [item2.iloc[2,0],item2.iloc[2,1],item2.iloc[2,2],item2.iloc[2,3],item2.iloc[2,4]], #香港恆生
            [item2.iloc[3,0],item2.iloc[3,1],item2.iloc[3,2],item2.iloc[3,3],item2.iloc[3,4]], #南韓綜合
            [item2.iloc[4,0],item2.iloc[4,1],item2.iloc[4,2],item2.iloc[4,3],item2.iloc[4,4]], #上海綜合
            [item2.iloc[7,0],item2.iloc[7,1],item2.iloc[7,2],item2.iloc[7,3],item2.iloc[7,4]], #A50期貨
            [item5.iloc[6,0],item5.iloc[6,1],item5.iloc[6,2],item5.iloc[6,3],item5.iloc[6,4]]  #印度指數
    ]

    #重要產業追蹤           
    ImportantIndustrayIndex = [
            [item9.iloc[0,0],item9.iloc[0,1],item9.iloc[0,2],item9.iloc[0,3]], #台積電ADR
            [item3.iloc[16,0],item3.iloc[16,1],item3.iloc[16,2],item3.iloc[16,3]], #GOOGLE
            [item3.iloc[17,0],item3.iloc[17,1],item3.iloc[17,2],item3.iloc[17,3]],  #蘋果
            [item3.iloc[20,0],item3.iloc[20,1],item3.iloc[20,2],item3.iloc[20,3]],  #Facebook
            [item3.iloc[18,0],item3.iloc[18,1],item3.iloc[18,2],item3.iloc[18,3]], #微軟
            [item3.iloc[6,0],item3.iloc[6,1],item3.iloc[6,2],item3.iloc[6,3]], #阿里巴巴
            [item3.iloc[8,0],item3.iloc[8,1],item3.iloc[8,2],item3.iloc[8,3]], #NBI生技

    ]


    #重要指標追蹤
    ImportantIndicatorsIndex = [
            [item0.iloc[1,0],item0.iloc[1,1],item0.iloc[1,2],item0.iloc[1,3]], #美元指數
            [item12.iloc[0,0],item12.iloc[0,1],item12.iloc[0,2],item12.iloc[0,3]], #比特幣
            [item12.iloc[1,0],item12.iloc[1,1],item12.iloc[1,2],item12.iloc[1,3]],  #乙太幣
            [item13.iloc[0,0],item13.iloc[0,1],item13.iloc[0,2],item13.iloc[0,3]],  #乾散裝型
            [item14.iloc[3,0],item14.iloc[3,1],item14.iloc[3,2],item14.iloc[3,3]],  #輕原油
            [item15.iloc[1,0],item15.iloc[1,1],item15.iloc[1,2],item15.iloc[1,3]],  #VIX
            [item16.iloc[4,0],item16.iloc[4,1],item16.iloc[4,2],item16.iloc[4,3]],  #黃金期
            [item16.iloc[5,0],item16.iloc[5,1],item16.iloc[5,2],item16.iloc[5,3]]   #黃金NT

    ]

    #匯率追蹤
    ExchangeRateIndex = [
            [item16.iloc[0,0],item16.iloc[0,1],item16.iloc[0,2],item16.iloc[0,3]], #歐元兌美元
            [item16.iloc[1,0],item16.iloc[1,1],item16.iloc[1,2],item16.iloc[1,3]],  #美元兌日圓
            [item16.iloc[3,0],item16.iloc[3,1],item16.iloc[3,2],item16.iloc[3,3]],  #美元兌人民幣
            [item17.iloc[0,0],item17.iloc[0,1],item17.iloc[0,2],item17.iloc[0,3],item17.iloc[0,4]],  #人民幣
            [item17.iloc[1,0],item17.iloc[1,1],item17.iloc[1,2],item17.iloc[1,3],item17.iloc[1,4]],  #日幣
            [item17.iloc[3,0],item17.iloc[3,1],item17.iloc[3,2],item17.iloc[3,3],item17.iloc[3,4]],  #美金
            [item17.iloc[5,0],item17.iloc[5,1],item17.iloc[5,2],item17.iloc[5,3],item17.iloc[5,4]]   #歐元 
    ]

    #歐美區追蹤
    EuropeAmericaIndex = [
            [item0.iloc[4,0],item0.iloc[4,1],item0.iloc[4,2],item0.iloc[4,3]],      #道瓊指數
            [item0.iloc[0,0],item0.iloc[0,1],item0.iloc[0,2],item0.iloc[0,3]],      #費城半導體     
            [item0.iloc[2,0],item0.iloc[2,1],item0.iloc[2,2],item0.iloc[2,3]],      #NASDAQ
            [item0.iloc[3,0],item0.iloc[3,1],item0.iloc[3,2],item0.iloc[3,3]],      #S&P500
            [item0.iloc[5,0],item0.iloc[5,1],item0.iloc[5,2],item0.iloc[5,3]],      #英國指數
            [item0.iloc[6,0],item0.iloc[6,1],item0.iloc[6,2],item0.iloc[6,3]],      #德國指數
            [item0.iloc[10,0],item0.iloc[10,1],item0.iloc[10,2],item0.iloc[10,3]]   #俄羅斯指數
    ]
    return render_to_response('internationIndex.html', locals())
