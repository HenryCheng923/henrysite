# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Company(models.Model):
    stockid = models.PositiveIntegerField(db_column='StockID', primary_key=True)  # Field name made lowercase.
    abbreviation = models.CharField(db_column='Abbreviation', unique=True, max_length=10, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', unique=True, max_length=128, blank=True, null=True)  # Field name made lowercase.
    employees = models.PositiveIntegerField(db_column='Employees', blank=True, null=True)  # Field name made lowercase.
    capital = models.BigIntegerField(db_column='Capital', blank=True, null=True)  # Field name made lowercase.
    industryname = models.CharField(db_column='IndustryName', max_length=16)  # Field name made lowercase.
    listeddate = models.CharField(db_column='ListedDate', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'

class All_sotck_daily_closing(models.Model):
    st_date = models.PositiveIntegerField(db_column='st_date', primary_key=True)  # Field name made lowercase.
    st_stockno = models.CharField(db_column='st_stockno', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    st_stockname = models.CharField(db_column='st_stockname', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    transaction_stockamount = models.BigIntegerField(db_column='transaction_stockamount', blank=True, null=True)  # Field name made lowercase.
    transaction_piecesamount = models.BigIntegerField(db_column='transaction_piecesamount', blank=True, null=True)  # Field name made lowercase.
    transaction_money = models.BigIntegerField(db_column='transaction_money', blank=True, null=True)  # Field name made lowercase.
    st_open = models.BigIntegerField(db_column='st_open', blank=True, null=True)  # Field name made lowercase.
    st_high = models.BigIntegerField(db_column='st_high', blank=True, null=True)  # Field name made lowercase.
    st_low = models.BigIntegerField(db_column='st_low', blank=True, null=True)  # Field name made lowercase.
    st_close = models.BigIntegerField(db_column='st_close', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'all_sotck_daily_closing'

class Three_legal(models.Model):
    st_date = models.PositiveIntegerField(db_column='st_date', primary_key=True)  # Field name made lowercase.
    dealer_buy = models.CharField(db_column='dealer_buy', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    dealer_sell = models.CharField(db_column='dealer_sell', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    dealer_diff = models.BigIntegerField(db_column='dealer_diff', blank=True, null=True)  # Field name made lowercase.
    dealer_heding_buy = models.BigIntegerField(db_column='dealer_heding_buy', blank=True, null=True)  # Field name made lowercase.
    dealer_heding_sell = models.BigIntegerField(db_column='dealer_heding_sell', blank=True, null=True)  # Field name made lowercase.
    dealer_heading_diff = models.BigIntegerField(db_column='dealer_heading_diff', blank=True, null=True)  # Field name made lowercase.
    it_buy = models.BigIntegerField(db_column='it_buy', blank=True, null=True)  # Field name made lowercase.
    it_sell = models.BigIntegerField(db_column='it_sell', blank=True, null=True)  # Field name made lowercase.
    it_diff = models.BigIntegerField(db_column='it_diff', blank=True, null=True)  # Field name made lowercase.
    foreign_investor_buy = models.BigIntegerField(db_column='foreign_investor_buy', blank=True, null=True)  # Field name made lowercase.
    foreign_investor_sell = models.BigIntegerField(db_column='foreign_investor_sell', blank=True, null=True)  # Field name made lowercase.
    foreign_investor_diff = models.BigIntegerField(db_column='foreign_investor_diff', blank=True, null=True)  # Field name made lowercase.
    foreign_investor_dealer_buy = models.BigIntegerField(db_column='foreign_investor_dealer_buy', blank=True, null=True)  # Field name made lowercase.
    foreign_investor_dealer_sell = models.BigIntegerField(db_column='foreign_investor_dealer_sell', blank=True, null=True)  # Field name made lowercase.
    foreign_investor_dealer_diff = models.BigIntegerField(db_column='foreign_investor_dealer_diff', blank=True, null=True)  # Field name made lowercase.
    total_buy = models.BigIntegerField(db_column='total_buy', blank=True, null=True)  # Field name made lowercase.
    total_sell = models.BigIntegerField(db_column='total_sell', blank=True, null=True)  # Field name made lowercase.
    total_diff = models.DecimalField(db_column='total_diff', max_digits=5, decimal_places=2, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'three_legal'


class Three_legal_overbuysell(models.Model):
    st_date = models.PositiveIntegerField(db_column='st_date', primary_key=True)  # Field name made lowercase.
    st_stockno = models.CharField(db_column='st_stockno', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    st_stockname = models.CharField(db_column='st_stockname', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    foreign_buy_amount = models.BigIntegerField(db_column='foreign_buy_amount', blank=True, null=True)  # Field name made lowercase.
    foreign_sell_amount = models.BigIntegerField(db_column='foreign_sell_amount', blank=True, null=True)  # Field name made lowercase.
    foreign_overbuysell = models.BigIntegerField(db_column='foreign_overbuysell', blank=True, null=True)  # Field name made lowercase.
    foreign_dealer_buy_amount = models.BigIntegerField(db_column='foreign_dealer_buy_amount', blank=True, null=True)  # Field name made lowercase.
    foreign_dealer_sell_amount = models.BigIntegerField(db_column='foreign_dealer_sell_amount', blank=True, null=True)  # Field name made lowercase.
    foreign_dealer_overbuysell= models.BigIntegerField(db_column='foreign_dealer_overbuysell', blank=True, null=True)  # Field name made lowercase.
    trust_buy_amount = models.BigIntegerField(db_column='trust_buy_amount', blank=True, null=True)  # Field name made lowercase.
    trust_sell_amount = models.BigIntegerField(db_column='trust_sell_amount', blank=True, null=True)  # Field name made lowercase.
    trust_overbuysell = models.BigIntegerField(db_column='trust_overbuysell', blank=True, null=True)  # Field name made lowercase.
    dealer_overbuysell = models.BigIntegerField(db_column='dealer_overbuysell', blank=True, null=True)  # Field name made lowercase.
    dealer_buysell_buy_amount = models.BigIntegerField(db_column='dealer_buysell_buy_amount', blank=True, null=True)  # Field name made lowercase.
    dealer_buysell_sell_amount = models.BigIntegerField(db_column='dealer_buysell_sell_amount', blank=True, null=True)  # Field name made lowercase.
    dealer_buysell_overbuysell = models.BigIntegerField(db_column='dealer_buysell_overbuysell', blank=True, null=True)  # Field name made lowercase.
    dealer_hedging_buy_amount = models.BigIntegerField(db_column='dealer_hedging_buy_amount', blank=True, null=True)  # Field name made lowercase.
    dealer_hedging_sell_amount = models.BigIntegerField(db_column='dealer_hedging_sell_amount', blank=True, null=True)  # Field name made lowercase.
    dealer_hedging_overbuysell = models.BigIntegerField(db_column='dealer_hedging_overbuysell')  # Field name made lowercase.
    three_legal_overbuysell = models.BigIntegerField(db_column='three_legal_overbuysell')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'three_legal_overbuysell'

class Wespai_p49048(models.Model):
    st_date = models.PositiveIntegerField(db_column='st_date', primary_key=True)  
    st_stockno = models.CharField(db_column='st_stockno', unique=True, max_length=20, blank=True, null=True)  
    st_stockname = models.CharField(db_column='st_stockname', unique=True, max_length=20, blank=True, null=True)  
    st_stockprice = models.BigIntegerField(db_column='st_stockprice', blank=True, null=True)  
    director_shareholding = models.BigIntegerField(db_column='director_shareholding', blank=True, null=True)  
    foreign_shareholding = models.BigIntegerField(db_column='foreign_shareholding', blank=True, null=True)  
    trust_shareholding = models.BigIntegerField(db_column='trust_shareholding', blank=True, null=True)  
    st_volume = models.BigIntegerField(db_column='st_volume', blank=True, null=True)  
    st_three_buysell = models.BigIntegerField(db_column='st_three_buysell', blank=True, null=True)  
    issued_number = models.BigIntegerField(db_column='issued_number', blank=True, null=True)  
    amount_of_capital = models.BigIntegerField(db_column='amount_of_capital', blank=True, null=True)
    trust_buysell = models.BigIntegerField(db_column='trust_buysell', blank=True, null=True) 
    foreign_buysell = models.BigIntegerField(db_column='foreign_buysell', blank=True, null=True) 
    industry_type = models.CharField(db_column='industry_type', unique=True, max_length=20, blank=True, null=True)
    trust_amount_day = models.BigIntegerField(db_column='trust_amount_day', blank=True, null=True) 
    trust_stock_quantity = models.BigIntegerField(db_column='trust_stock_quantity', blank=True, null=True) 
    trust_stock_totalAmount = models.BigIntegerField(db_column='trust_stock_totalAmount', blank=True, null=True) 
    trust_buysell_shareCapital_ratio = models.DecimalField(db_column='trust_buysell_shareCapital_ratio',max_digits=5, decimal_places=2, null=True) 
    foreign_amount_day = models.BigIntegerField(db_column='foreign_amount_day', blank=True, null=True) 
    foreign_stock_quantity = models.BigIntegerField(db_column='foreign_stock_quantity', blank=True, null=True) 
    foreign_stock_totalAmount = models.BigIntegerField(db_column='foreign_stock_totalAmount', blank=True, null=True) 
    foreign_buysell_shareCapital_ratio = models.DecimalField(db_column='foreign_buysell_shareCapital_ratio', max_digits=5, decimal_places=2, null=True)  
    
    class Meta:
        managed = False
        db_table = 'wespai_p49048'


class All_stock_daily_closing(models.Model):
    st_date = models.PositiveIntegerField(db_column='st_date', primary_key=True)  
    st_stockno = models.CharField(db_column='st_stockno', unique=True, max_length=20, blank=True, null=True)  
    st_stockname = models.CharField(db_column='st_stockname', unique=True, max_length=20, blank=True, null=True)  
    transaction_stockamount = models.BigIntegerField(db_column='transaction_stockamount', blank=True, null=True)  
    transaction_piecesamount = models.BigIntegerField(db_column='transaction_piecesamount', blank=True, null=True)  
    transaction_money = models.BigIntegerField(db_column='transaction_money', blank=True, null=True)  
    st_open = models.BigIntegerField(db_column='st_open', blank=True, null=True)  
    st_high = models.BigIntegerField(db_column='st_high', blank=True, null=True)  
    st_low = models.BigIntegerField(db_column='st_low', blank=True, null=True)  
    st_close = models.BigIntegerField(db_column='st_close', blank=True, null=True)
    change_extent = models.BigIntegerField(db_column='change_extent', blank=True, null=True) 
    
    class Meta:
        managed = False
        db_table = 'all_stock_daily_closing'


class Call_warrant(models.Model):
    st_date = models.PositiveIntegerField(db_column='st_date', primary_key=True)  
    st_stockno_call_warrant = models.CharField(db_column='st_stockno_call_warrant', unique=True, max_length=20, blank=True, null=True)  
    st_stockname_call_warrant = models.CharField(db_column='st_stockname_call_warrant', unique=True, max_length=20, blank=True, null=True)  
    st_numberOfShares_call_warrant = models.BigIntegerField(db_column='st_numberOfShares_call_warrant', blank=True, null=True)  
    st_count_call_warrant = models.BigIntegerField(db_column='st_count_call_warrant', blank=True, null=True)  
    st_amount_call_warrant = models.BigIntegerField(db_column='st_amount_call_warrant', blank=True, null=True)  
    st_close_call_warrant = models.DecimalField(db_column='st_close_call_warrant', max_digits=5, decimal_places=2, null=True)   
    st_stockno = models.CharField(db_column='st_stockno', unique=True, max_length=20, blank=True, null=True)  
    st_stockname = models.CharField(db_column='st_stockname', unique=True, max_length=20, blank=True, null=True)  
    st_close = models.DecimalField(db_column='st_close', max_digits=5, decimal_places=2, null=True)   
    
    class Meta:
        managed = False
        db_table = 'call_warrant'