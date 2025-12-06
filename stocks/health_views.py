"""
Health check views for monitoring application status
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
from stocks.models import Stocks
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Health check endpoint for load balancer and monitoring
    """
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'checks': {}
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check if we have stock data
    try:
        stock_count = Stocks.objects.count()
        health_status['checks']['stock_data'] = {
            'status': 'healthy' if stock_count > 0 else 'warning',
            'count': stock_count
        }
        if stock_count == 0:
            health_status['status'] = 'degraded'
    except Exception as e:
        health_status['checks']['stock_data'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check cache (if available)
    try:
        cache.set('health_check', 'test', 30)
        if cache.get('health_check') == 'test':
            health_status['checks']['cache'] = 'healthy'
        else:
            health_status['checks']['cache'] = 'unhealthy'
    except Exception as e:
        health_status['checks']['cache'] = f'unavailable: {str(e)}'
    
    # Return appropriate HTTP status
    if health_status['status'] == 'unhealthy':
        return JsonResponse(health_status, status=503)
    elif health_status['status'] == 'degraded':
        return JsonResponse(health_status, status=200)
    else:
        return JsonResponse(health_status, status=200)


def readiness_check(request):
    """
    Readiness check for Kubernetes/Docker
    """
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if we have basic data
        if Stocks.objects.count() == 0:
            return JsonResponse({
                'status': 'not_ready',
                'reason': 'No stock data available'
            }, status=503)
        
        return JsonResponse({
            'status': 'ready',
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'reason': str(e)
        }, status=503)


def liveness_check(request):
    """
    Liveness check for Kubernetes/Docker
    """
    return JsonResponse({
        'status': 'alive',
        'timestamp': timezone.now().isoformat()
    })
