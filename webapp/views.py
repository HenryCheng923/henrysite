from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from webapp.models import Company #呼叫webapp資料夾底下的models 的company函數，用來連結資料庫的方法
from webapp.models import All_sotck_daily_closing 
from webapp.models import Three_legal
from webapp.models import Three_legal_overbuysell
from webapp.models import Wespai_p49048  
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from django.db.models import Q

from E_14_2 import main as E_14_2_main

def pylinkweb(request):
	return HttpResponse("Django讓python能方便連結網頁")

def index(request):
    now = datetime.now()
    return render(request,'index.html',locals())

#年金計算
def fv(request):
    return render(request,'E_10_1.html',{})
def result(request):
    pv=int(request.GET['amount'])
    i=float(request.GET['rate'])
    n=int(request.GET['period'])
    fv=str((pv*((1+i)**n)))
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
        
        #getvalue = Three_legal_overbuysell.objects.all().order_by("st_date")[:10]
        return render(request,'do_search.html', locals())
    else:
        return redirect("/three_legal_overbuysell/")
    #stocknovalue = request.GET.get('st_stockno')
    #stocknovalue = request.GET['st_stockno']

#投本比資料
def shareCapital_ratio(request):
    date = 20191128
    get_db_trust_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = date,  st_stockprice__gt = 30,  trust_stock_totalAmount__gt = 5000000, st_volume__gt = 1000) 
    get_db_foreign_buysell_shareCapital_ratio = Wespai_p49048.objects.filter(st_date = date,  st_stockprice__gt = 30,  foreign_stock_totalAmount__gt = 500000000, st_volume__gt = 1000)
    #SELECT * FROM stockdatabase.wespai_p49048 where trust_buysell_shareCapital_ratio > 0.1 and foreign_buysell_shareCapital_ratio > 0 and st_stockprice > 30 and trust_stock_totalAmount > 5000000 and st_volume >1000;
    #trust_buysell_shareCapital_ratio__range = [1, 3] , foreign_buysell_shareCapital_ratio__gt = 0.1,
    return render_to_response('shareCapital_ratio.html', locals())
