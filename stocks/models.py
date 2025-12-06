from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, help_text="Phone number with country code")
    address = models.CharField(max_length=500)
    pancard_number = models.CharField(max_length=30, unique=True, help_text="PAN Card Number")
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    pancard_image = models.ImageField(upload_to='pancard_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
    class Meta:
        verbose_name = "User Information"
        verbose_name_plural = "User Information"

# ImageFiled in Models
#  pip  install pillow
#  media url in setting
#  static url  in urls.py

class Stocks(models.Model):
    ticker = models.CharField(max_length=10, unique=True, db_index=True, help_text="Stock ticker symbol")
    name = models.CharField(max_length=300, db_index=True)
    description = models.TextField(max_length=5000, blank=True)
    curr_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Current stock price"
    )
    market_cap = models.BigIntegerField(null=True, blank=True, help_text="Market capitalization")
    sector = models.CharField(max_length=100, blank=True, default='', help_text="Stock sector")
    industry = models.CharField(max_length=100, blank=True, default='', help_text="Stock industry")
    volume = models.BigIntegerField(default=0, help_text="Trading volume")
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Is stock actively traded")

    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['ticker']


# Fk is many to one

class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Average purchase price"
    )
    purchase_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of shares owned"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    @property
    def current_value(self):
        return self.stock.curr_price * self.purchase_quantity
    
    @property
    def invested_value(self):
        return self.purchase_price * self.purchase_quantity
    
    @property
    def gain_loss(self):
        return self.current_value - self.invested_value
    
    @property
    def gain_loss_percentage(self):
        if self.invested_value > 0:
            return (self.gain_loss / self.invested_value) * 100
        return 0
    
    def __str__(self):
        return f"{self.user.username} - {self.stock.ticker} ({self.purchase_quantity} shares)"
    
    class Meta:
        unique_together = ('user', 'stock')
        verbose_name = "User Stock Position"
        verbose_name_plural = "User Stock Positions"




class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    stock_symbol = models.CharField(max_length=10, db_index=True)
    stock_name = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price per share"
    )
    type = models.CharField(max_length=4, choices=TRANSACTION_TYPES, db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    
    @property
    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.get_type_display()} {self.quantity} of {self.stock_symbol} by {self.user.username} on {self.date.strftime("%Y-%m-%d")}'
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=300)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('user', 'stock_symbol')

    def __str__(self):
        return f'{self.user.username} watches {self.stock_symbol}'


class PriceAlert(models.Model):
    ALERT_TYPES = [
        ('ABOVE', 'Price Above'),
        ('BELOW', 'Price Below'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('TRIGGERED', 'Triggered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_alerts')
    stock_symbol = models.CharField(max_length=10, db_index=True)
    stock_name = models.CharField(max_length=300)
    alert_type = models.CharField(max_length=5, choices=ALERT_TYPES)
    target_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Price Alert"
        verbose_name_plural = "Price Alerts"
    
    def __str__(self):
        return f'{self.user.username} - {self.stock_symbol} {self.alert_type} ${self.target_price}'


class StockComparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="Comparison name")
    stocks = models.TextField(help_text="Comma-separated list of stock symbols")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Stock Comparison"
        verbose_name_plural = "Stock Comparisons"
    
    def __str__(self):
        return f'{self.user.username} - {self.name}'
    
    def get_stocks_list(self):
        """Return stocks as a list"""
        return [s.strip() for s in self.stocks.split(',') if s.strip()]
    
    def set_stocks_list(self, stocks_list):
        """Set stocks from a list"""
        self.stocks = ','.join(stocks_list)


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    email_notifications = models.BooleanField(default=True, help_text="Receive email notifications")
    price_alert_notifications = models.BooleanField(default=True, help_text="Receive price alert notifications")
    transaction_notifications = models.BooleanField(default=True, help_text="Receive transaction notifications")
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    default_currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"
    
    def __str__(self):
        return f'{self.user.username} preferences'


