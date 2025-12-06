from django.contrib import admin

# Register your models here.
from .models import (
    Stocks, UserInfo, UserStock, Transaction, 
    Watchlist, PriceAlert, StockComparison, UserPreference
)

# Customize admin site header
admin.site.site_header = "StockFolio Admin"
admin.site.site_title = "StockFolio Admin Portal"
admin.site.index_title = "Welcome to StockFolio Administration"


@admin.register(Stocks)
class StocksAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'name', 'curr_price', 'sector', 'volume', 'last_updated', 'is_active']
    list_filter = ['sector', 'is_active', 'last_updated']
    search_fields = ['ticker', 'name', 'sector']
    list_per_page = 50
    ordering = ['ticker']


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'pancard_number', 'created_at']
    search_fields = ['user__username', 'phone_number', 'pancard_number']
    list_filter = ['created_at']


@admin.register(UserStock)
class UserStockAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'purchase_quantity', 'purchase_price', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'stock__ticker', 'stock__name']
    raw_id_fields = ['user', 'stock']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock_symbol', 'type', 'quantity', 'price', 'date']
    list_filter = ['type', 'date']
    search_fields = ['user__username', 'stock_symbol', 'stock_name']
    date_hierarchy = 'date'
    list_per_page = 100


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock_symbol', 'stock_name', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'stock_symbol', 'stock_name']


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock_symbol', 'alert_type', 'target_price', 'status', 'created_at']
    list_filter = ['alert_type', 'status', 'created_at']
    search_fields = ['user__username', 'stock_symbol']
    date_hierarchy = 'created_at'


@admin.register(StockComparison)
class StockComparisonAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'name']


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'price_alert_notifications', 'theme']
    list_filter = ['email_notifications', 'theme']
    search_fields = ['user__username']