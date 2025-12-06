"""
Enhanced views for new features: Price Alerts, Stock Comparison, User Preferences
"""
import logging
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Q
from django.utils import timezone

from .models import (
    Stocks, PriceAlert, StockComparison, 
    UserPreference, Watchlist, UserStock
)
from .services import stock_service

logger = logging.getLogger(__name__)


@login_required
def price_alerts_view(request):
    """View and manage price alerts"""
    alerts = PriceAlert.objects.filter(user=request.user).select_related()
    
    # Enhance alerts with current prices
    enhanced_alerts = []
    for alert in alerts:
        try:
            stock_data = stock_service.get_stock_data(alert.stock_symbol)
            current_price = stock_data['current_price'] if stock_data else 0
            
            # Check if alert should be triggered
            if alert.status == 'ACTIVE':
                if (alert.alert_type == 'ABOVE' and current_price >= alert.target_price) or \
                   (alert.alert_type == 'BELOW' and current_price <= alert.target_price):
                    alert.status = 'TRIGGERED'
                    alert.triggered_at = timezone.now()
                    alert.save()
            
            enhanced_alerts.append({
                'alert': alert,
                'current_price': current_price,
                'difference': float(current_price - alert.target_price) if current_price else 0
            })
        except Exception as e:
            logger.error(f"Error processing alert {alert.id}: {str(e)}")
            enhanced_alerts.append({
                'alert': alert,
                'current_price': 0,
                'difference': 0
            })
    
    context = {
        'alerts': enhanced_alerts,
        'active_count': alerts.filter(status='ACTIVE').count(),
        'triggered_count': alerts.filter(status='TRIGGERED').count()
    }
    return render(request, 'price_alerts.html', context)


@login_required
@require_POST
def create_price_alert(request):
    """Create a new price alert"""
    try:
        stock_symbol = request.POST.get('stock_symbol', '').upper()
        alert_type = request.POST.get('alert_type')
        target_price = Decimal(request.POST.get('target_price'))
        
        # Validate stock exists
        stock = Stocks.objects.filter(ticker=stock_symbol).first()
        if not stock:
            messages.error(request, f"Stock {stock_symbol} not found.")
            return redirect('price_alerts')
        
        # Create alert
        PriceAlert.objects.create(
            user=request.user,
            stock_symbol=stock.ticker,
            stock_name=stock.name,
            alert_type=alert_type,
            target_price=target_price,
            status='ACTIVE'
        )
        
        messages.success(request, f"Price alert created for {stock.name} at ${target_price}")
        logger.info(f"User {request.user.username} created alert for {stock_symbol}")
        
    except Exception as e:
        logger.error(f"Error creating price alert: {str(e)}")
        messages.error(request, "Failed to create price alert. Please try again.")
    
    return redirect('price_alerts')


@login_required
@require_POST
def delete_price_alert(request, alert_id):
    """Delete a price alert"""
    try:
        alert = get_object_or_404(PriceAlert, id=alert_id, user=request.user)
        alert.delete()
        messages.success(request, "Price alert deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting alert: {str(e)}")
        messages.error(request, "Failed to delete alert.")
    
    return redirect('price_alerts')


@login_required
def stock_comparison_view(request):
    """Compare multiple stocks side by side"""
    comparisons = StockComparison.objects.filter(user=request.user)
    
    # Get stocks to compare from query params
    symbols = request.GET.getlist('symbols')
    comparison_data = []
    
    if symbols:
        for symbol in symbols[:5]:  # Limit to 5 stocks
            try:
                stock = Stocks.objects.filter(ticker=symbol.upper()).first()
                if stock:
                    stock_data = stock_service.get_stock_data(symbol.upper())
                    if stock_data:
                        comparison_data.append({
                            'symbol': stock.ticker,
                            'name': stock.name,
                            'current_price': stock_data['current_price'],
                            'day_change': stock_data.get('day_change', 0),
                            'day_change_percent': stock_data.get('day_change_percent', 0),
                            'volume': stock_data.get('volume', 0),
                            'market_cap': stock_data.get('market_cap', 0),
                            'sector': stock_data.get('sector', 'N/A'),
                            'pe_ratio': stock_data.get('pe_ratio', 'N/A'),
                        })
            except Exception as e:
                logger.error(f"Error comparing {symbol}: {str(e)}")
    
    context = {
        'comparisons': comparisons,
        'comparison_data': comparison_data,
        'symbols': symbols
    }
    return render(request, 'stock_comparison.html', context)


@login_required
@require_POST
def save_comparison(request):
    """Save a stock comparison"""
    try:
        name = request.POST.get('name')
        symbols = request.POST.getlist('symbols')
        
        if not name or not symbols:
            messages.error(request, "Please provide a name and select stocks.")
            return redirect('stock_comparison')
        
        comparison = StockComparison(user=request.user, name=name)
        comparison.set_stocks_list(symbols)
        comparison.save()
        
        messages.success(request, f"Comparison '{name}' saved successfully.")
    except Exception as e:
        logger.error(f"Error saving comparison: {str(e)}")
        messages.error(request, "Failed to save comparison.")
    
    return redirect('stock_comparison')


@login_required
def load_comparison(request, comparison_id):
    """Load a saved comparison"""
    try:
        comparison = get_object_or_404(StockComparison, id=comparison_id, user=request.user)
        stocks_list = comparison.get_stocks_list()
        symbols = '&'.join([f'symbols={s}' for s in stocks_list])
        return redirect(f'/stock-comparison/?{symbols}')
    except Exception as e:
        logger.error(f"Error loading comparison: {str(e)}")
        messages.error(request, "Failed to load comparison.")
        return redirect('stock_comparison')


@login_required
def user_preferences_view(request):
    """View and update user preferences"""
    preferences, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            preferences.email_notifications = request.POST.get('email_notifications') == 'on'
            preferences.price_alert_notifications = request.POST.get('price_alert_notifications') == 'on'
            preferences.transaction_notifications = request.POST.get('transaction_notifications') == 'on'
            preferences.theme = request.POST.get('theme', 'light')
            preferences.save()
            
            messages.success(request, "Preferences updated successfully.")
        except Exception as e:
            logger.error(f"Error updating preferences: {str(e)}")
            messages.error(request, "Failed to update preferences.")
    
    context = {'preferences': preferences}
    return render(request, 'user_preferences.html', context)


@login_required
def dashboard_analytics(request):
    """Enhanced dashboard with analytics"""
    user = request.user
    
    # Get portfolio data
    user_stocks = UserStock.objects.select_related('stock').filter(user=user)
    
    total_value = 0
    invested = 0
    portfolio_data = []
    
    for item in user_stocks:
        stock_data = stock_service.get_stock_data(item.stock.ticker)
        current_price = stock_data['current_price'] if stock_data else float(item.stock.curr_price)
        
        stock_value = item.purchase_quantity * Decimal(str(current_price))
        invested_value = item.purchase_quantity * item.purchase_price
        gain_loss = stock_value - invested_value
        gain_loss_pct = (gain_loss / invested_value * 100) if invested_value > 0 else 0
        
        total_value += stock_value
        invested += invested_value
        
        portfolio_data.append({
            'stock': item.stock,
            'quantity': item.purchase_quantity,
            'current_price': current_price,
            'purchase_price': float(item.purchase_price),
            'current_value': float(stock_value),
            'invested_value': float(invested_value),
            'gain_loss': float(gain_loss),
            'gain_loss_pct': float(gain_loss_pct)
        })
    
    total_gain_loss = total_value - invested
    total_gain_loss_pct = (total_gain_loss / invested * 100) if invested > 0 else 0
    
    # Get watchlist count
    watchlist_count = Watchlist.objects.filter(user=user).count()
    
    # Get active alerts count
    active_alerts = PriceAlert.objects.filter(user=user, status='ACTIVE').count()
    
    context = {
        'portfolio_data': portfolio_data,
        'total_value': float(total_value),
        'invested': float(invested),
        'total_gain_loss': float(total_gain_loss),
        'total_gain_loss_pct': float(total_gain_loss_pct),
        'watchlist_count': watchlist_count,
        'active_alerts': active_alerts,
        'portfolio_count': len(portfolio_data)
    }
    
    return render(request, 'dashboard_analytics.html', context)


@login_required
def stock_search_api(request):
    """API endpoint for stock search"""
    query = request.GET.get('q', '').upper()
    
    if len(query) < 1:
        return JsonResponse({'results': []})
    
    stocks = Stocks.objects.filter(
        Q(ticker__icontains=query) | Q(name__icontains=query)
    )[:10]
    
    results = [{
        'ticker': stock.ticker,
        'name': stock.name,
        'price': float(stock.curr_price),
        'sector': stock.sector
    } for stock in stocks]
    
    return JsonResponse({'results': results})
