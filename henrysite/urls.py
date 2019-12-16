"""henrysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp import views #使用webapp底下的views要import views才可以使用



urlpatterns = [
    path('',views.index),
    path('admin/', admin.site.urls),
    path('gogo/', views.pylinkweb), #呼叫gogo路徑底下 views資料夾的pylinkweb函數
    
    path('test/', views.test),
    #年金計算
    path('fv/', views.fv),
    path('result/', views.result),

    #公司股票資料
    path('company/',views.company),
    path('company/insert/',views.insert),
    path('do_insert/',views.do_insert),
    path('company/detail/<int:stockid>/',views.detail),
    path('company/update/<int:stockid>/',views.update),
    path('do_update/',views.do_update),
    path('company/delete/<int:stockid>/',views.delete),
    path('do_delete/',views.do_delete),

    #股票每日資訊
    path('daily_if/',views.all_sotck_daily_closing),
    
    #
    path('E_14_2/',views.E_14_2),
    path('E_14_2_Py/',views.E_14_2_Py),

    #three_legal
    path('three_legal/',views.three_legal),

    #three_legal_overbuysell
    path('three_legal_overbuysell/',views.three_legal_overbuysell),
    path('do_search/',views.do_search),

    #shareCapital_ratio.html
    path('shareCapital_ratio/',views.shareCapital_ratio),

    #call_warrant.html
    path('call_warrant/',views.call_warrant),

    #外資、投信、自營買賣超比
    path('foreign_buy_shareCapital_ratio/', views.foreign_buy_shareCapital_ratio),
    path('foreign_sell_shareCapital_ratio/', views.foreign_sell_shareCapital_ratio),
    path('trust_buy_shareCapital_ratio/', views.trust_buy_shareCapital_ratio),
    path('trust_sell_shareCapital_ratio/', views.trust_sell_shareCapital_ratio),
    path('dealer_buy_shareCapital_ratio/', views.dealer_buy_shareCapital_ratio),
    path('dealer_sell_shareCapital_ratio/', views.dealer_sell_shareCapital_ratio),

    #資、投信、自營累計買賣超比
    path('foreign_buyAcc_shareCapital_ratio/', views.foreign_buyAcc_shareCapital_ratio),
    path('trust_buyAcc_shareCapital_ratio/', views.trust_buyAcc_shareCapital_ratio),
    path('dealer_buyAcc_shareCapital_ratio/', views.dealer_buyAcc_shareCapital_ratio),
]
