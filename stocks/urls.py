"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    index, populate_stock_data, stocks, loginView, logoutView, register,
    buy, sell, transaction_history, portfolio_dashboard,
    watchlist_view, add_to_watchlist, remove_from_watchlist,
    get_stock_price_api, update_watchlist_prices_api, stock_detail
)
from .health_views import health_check, readiness_check, liveness_check
from .enhanced_views import (
    price_alerts_view, create_price_alert, delete_price_alert,
    stock_comparison_view, save_comparison, load_comparison,
    user_preferences_view, dashboard_analytics, stock_search_api
)

urlpatterns = [
    # Main pages
    path('', index, name='index'),
    path('dashboard/', dashboard_analytics, name='dashboard_analytics'),
    path('stocks/', stocks, name='stocks'),
    path('stock/<str:ticker>/', stock_detail, name='stock_detail'),  # Stock detail page
    path('admin/populate-stocks/', populate_stock_data, name='populate_stock_data'),
    
    # Authentication
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', register, name='register'),
    
    # Trading
    path('buy/<int:id>/', buy, name='buy'),
    path('sell/<int:id>/', sell, name='sell'),
    path('transaction_history/', transaction_history, name='transaction_history'),
    path('portfolio_dashboard/', portfolio_dashboard, name='portfolio_dashboard'),
    
    # Watchlist
    path('watchlist/', watchlist_view, name='watchlist_view'),
    path('add_to_watchlist/<str:stock_symbol>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<str:stock_symbol>/', remove_from_watchlist, name='remove_from_watchlist'),
    
    # Price Alerts (NEW)
    path('price-alerts/', price_alerts_view, name='price_alerts'),
    path('price-alerts/create/', create_price_alert, name='create_price_alert'),
    path('price-alerts/delete/<int:alert_id>/', delete_price_alert, name='delete_price_alert'),
    
    # Stock Comparison (NEW)
    path('stock-comparison/', stock_comparison_view, name='stock_comparison'),
    path('stock-comparison/save/', save_comparison, name='save_comparison'),
    path('stock-comparison/load/<int:comparison_id>/', load_comparison, name='load_comparison'),
    
    # User Preferences (NEW)
    path('preferences/', user_preferences_view, name='user_preferences'),
    
    # API endpoints for real-time data
    path('api/stock/<str:symbol>/price/', get_stock_price_api, name='stock_price_api'),
    path('api/watchlist/update-prices/', update_watchlist_prices_api, name='update_watchlist_prices_api'),
    path('api/stock/search/', stock_search_api, name='stock_search_api'),
    
    # Health check endpoints
    path('api/health/', health_check, name='health_check'),
    path('api/ready/', readiness_check, name='readiness_check'),
    path('api/alive/', liveness_check, name='liveness_check'),
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
