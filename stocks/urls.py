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
    get_stock_price_api, update_watchlist_prices_api
)
from .health_views import health_check, readiness_check, liveness_check

urlpatterns = [
    path('', index, name='index'),
    path('stocks/', stocks, name='stocks'),
    path('admin/populate-stocks/', populate_stock_data, name='populate_stock_data'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', register, name='register'),
    path('buy/<int:id>/', buy, name='buy'),
    path('sell/<int:id>/', sell, name='sell'),
    path('transaction_history/', transaction_history, name='transaction_history'),
    path('portfolio_dashboard/', portfolio_dashboard, name='portfolio_dashboard'),
    path('watchlist/', watchlist_view, name='watchlist_view'),
    path('add_to_watchlist/<str:stock_symbol>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<str:stock_symbol>/', remove_from_watchlist, name='remove_from_watchlist'),
    
    # API endpoints for real-time data
    path('api/stock/<str:symbol>/price/', get_stock_price_api, name='stock_price_api'),
    path('api/watchlist/update-prices/', update_watchlist_prices_api, name='update_watchlist_prices_api'),
    
    # Health check endpoints
    path('api/health/', health_check, name='health_check'),
    path('api/ready/', readiness_check, name='readiness_check'),
    path('api/alive/', liveness_check, name='liveness_check'),
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
