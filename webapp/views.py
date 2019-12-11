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


import json
import datetime

import pymysql
MYSQL_HOST = 'localhost'
MYSQL_DB = 'stockdatabase'
MYSQL_USER = 'root'
MYSQL_PASS = 'b123456'
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


def connect_mysql():  #連線資料庫
    global connect, cursor
    connect = pymysql.connect(host = MYSQL_HOST, db = MYSQL_DB, user = MYSQL_USER, password = MYSQL_PASS,
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
        start_date = date
        #finish_date = 20191210
        stock_price = 30
        foreign_stock_totalAmount = 5000000
        change_extent = 0.03
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = 0.2

    get_db_foreign_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gt = stock_price,  foreign_stock_totalAmount__gt = foreign_stock_totalAmount, st_volume__gte = st_volume, foreign_buysell_shareCapital_ratio__gte = foreign_shareCapital_ratio, trust_buysell_shareCapital_ratio__gt = trust_shareCapital_ratio)\
                                                                        .order_by("-foreign_buysell_shareCapital_ratio")

    return render_to_response('foreign_buy_shareCapital_ratio.html', locals())


#外資比賣超資料頁面
def foreign_sell_shareCapital_ratio(request):
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
        start_date = date
        #finish_date = 20191210
        stock_price = 30
        foreign_stock_totalAmount = 5000000
        change_extent = 0.03
        st_volume = 1000
        trust_shareCapital_ratio = 0
        foreign_shareCapital_ratio = -0.2

    get_db_foreign_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gt = stock_price,  foreign_stock_totalAmount__gte = foreign_stock_totalAmount, st_volume__gte = st_volume, foreign_buysell_shareCapital_ratio__lte = foreign_shareCapital_ratio, trust_buysell_shareCapital_ratio__lt = trust_shareCapital_ratio)\
                                                                        .order_by("foreign_buysell_shareCapital_ratio")

    return render_to_response('foreign_sell_shareCapital_ratio.html', locals())


#投信比買超資料頁面
def trust_buy_shareCapital_ratio(request):
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
        start_date = date
        #finish_date = 20191210
        stock_price = 30
        trust_stock_totalAmount = 5000000
        change_extent = 0.03
        st_volume = 1000
        trust_shareCapital_ratio = 0.1
        foreign_shareCapital_ratio = 0

    get_db_trust_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  trust_stock_totalAmount__gte = trust_stock_totalAmount, st_volume__gte = st_volume, trust_buysell_shareCapital_ratio__gte = trust_shareCapital_ratio ,foreign_buysell_shareCapital_ratio__gt = foreign_shareCapital_ratio)\
                                                            .order_by("-trust_buysell_shareCapital_ratio")

    return render_to_response('trust_buy_shareCapital_ratio.html', locals())


#投信比賣超資料頁面
def trust_sell_shareCapital_ratio(request):
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
        start_date = date
        #finish_date = 20191210
        stock_price = 30
        trust_stock_totalAmount = 5000000
        change_extent = 0.03
        st_volume = 1000
        trust_shareCapital_ratio = -0.1
        foreign_shareCapital_ratio = 0

    get_db_trust_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = start_date,  st_stockprice__gte = stock_price,  trust_stock_totalAmount__gte = trust_stock_totalAmount, st_volume__gte = st_volume, trust_buysell_shareCapital_ratio__lte = trust_shareCapital_ratio ,foreign_buysell_shareCapital_ratio__lt = foreign_shareCapital_ratio)\
                                                            .order_by("trust_buysell_shareCapital_ratio")

    return render_to_response('trust_sell_shareCapital_ratio.html', locals())