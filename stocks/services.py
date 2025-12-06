"""
Stock data services for fetching and processing stock market data.
"""
import logging
import requests
import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Any
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)


class StockDataService:
    """Service for fetching stock data from various APIs"""
    
    def __init__(self):
        self.tiingo_token = getattr(settings, 'STOCK_API_SETTINGS', {}).get('TIINGO_API_TOKEN')
        self.alpha_vantage_key = getattr(settings, 'STOCK_API_SETTINGS', {}).get('ALPHA_VANTAGE_API_KEY')
        self.finnhub_key = getattr(settings, 'STOCK_API_SETTINGS', {}).get('FINNHUB_API_KEY')
        self.cache_timeout = getattr(settings, 'STOCK_API_SETTINGS', {}).get('CACHE_TIMEOUT', 300)
        
    def get_stock_data(self, symbol: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive stock data for a given symbol.
        """
        cache_key = f"stock_data_{symbol}"
        
        if use_cache:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Retrieved cached data for {symbol}")
                return cached_data
        
        try:
            # Try yfinance first (free and reliable)
            stock_data = self._get_yfinance_data(symbol)
            
            if not stock_data and self.tiingo_token:
                # Fallback to Tiingo
                stock_data = self._get_tiingo_data(symbol)
            
            if stock_data and use_cache:
                cache.set(cache_key, stock_data, self.cache_timeout)
                logger.info(f"Cached data for {symbol}")
                
            return stock_data
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            return None
    
    def _get_yfinance_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch stock data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                return None
                
            current_price = hist['Close'].iloc[-1]
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', symbol),
                'current_price': float(current_price),
                'previous_close': float(info.get('previousClose', current_price)),
                'day_change': float(current_price - info.get('previousClose', current_price)),
                'day_change_percent': float((current_price - info.get('previousClose', current_price)) / info.get('previousClose', current_price) * 100) if info.get('previousClose') else 0,
                'volume': int(info.get('volume', 0)),
                'market_cap': info.get('marketCap', 0),
                'description': info.get('longBusinessSummary', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'last_updated': datetime.now().isoformat(),
                'source': 'yfinance'
            }
            
        except Exception as e:
            logger.warning(f"yfinance failed for {symbol}: {str(e)}")
            return None
    
    def _get_tiingo_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch stock data using Tiingo API"""
        if not self.tiingo_token:
            return None
            
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Get stock metadata
            meta_url = f"https://api.tiingo.com/tiingo/daily/{symbol}?token={self.tiingo_token}"
            price_url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?token={self.tiingo_token}"
            
            meta_response = requests.get(meta_url, headers=headers, timeout=10)
            price_response = requests.get(price_url, headers=headers, timeout=10)
            
            if meta_response.status_code == 200 and price_response.status_code == 200:
                metadata = meta_response.json()
                price_data = price_response.json()
                
                if price_data:
                    latest_price = price_data[0]
                    current_price = latest_price['close']
                    previous_close = latest_price.get('prevClose', current_price)
                    
                    return {
                        'symbol': metadata['ticker'],
                        'name': metadata['name'],
                        'current_price': float(current_price),
                        'previous_close': float(previous_close),
                        'day_change': float(current_price - previous_close),
                        'day_change_percent': float((current_price - previous_close) / previous_close * 100) if previous_close else 0,
                        'volume': int(latest_price.get('volume', 0)),
                        'description': metadata.get('description', ''),
                        'last_updated': datetime.now().isoformat(),
                        'source': 'tiingo'
                    }
                    
        except Exception as e:
            logger.warning(f"Tiingo API failed for {symbol}: {str(e)}")
            
        return None
    
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get data for multiple stocks"""
        results = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol)
            if data:
                results[symbol] = data
        return results
    
    def get_stock_history(self, symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """Get historical stock data"""
        cache_key = f"stock_history_{symbol}_{period}"
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if not hist.empty:
                cache.set(cache_key, hist, self.cache_timeout)
                return hist
                
        except Exception as e:
            logger.error(f"Error fetching history for {symbol}: {str(e)}")
        
        return None
    
    def search_stocks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for stocks by name or symbol"""
        # This is a simplified search - in production, you might want to use
        # a more sophisticated search API
        nasdaq_symbols = [
            {"symbol": "AAPL", "name": "Apple Inc."},
            {"symbol": "MSFT", "name": "Microsoft Corporation"},
            {"symbol": "GOOGL", "name": "Alphabet Inc."},
            {"symbol": "AMZN", "name": "Amazon.com Inc."},
            {"symbol": "TSLA", "name": "Tesla Inc."},
            {"symbol": "META", "name": "Meta Platforms Inc."},
            {"symbol": "NVDA", "name": "NVIDIA Corporation"},
            {"symbol": "NFLX", "name": "Netflix Inc."},
            {"symbol": "ADBE", "name": "Adobe Inc."},
            {"symbol": "CRM", "name": "Salesforce Inc."},
        ]
        
        query = query.lower()
        results = []
        
        for stock in nasdaq_symbols:
            if (query in stock["symbol"].lower() or 
                query in stock["name"].lower()):
                results.append(stock)
                if len(results) >= limit:
                    break
        
        return results


class PortfolioAnalyzer:
    """Service for analyzing portfolio performance"""
    
    def __init__(self):
        self.stock_service = StockDataService()
    
    def calculate_portfolio_metrics(self, portfolio_data: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics"""
        total_value = 0
        total_invested = 0
        total_gain_loss = 0
        
        for position in portfolio_data:
            current_price = position.get('current_price', 0)
            quantity = position.get('quantity', 0)
            avg_purchase_price = position.get('avg_purchase_price', 0)
            
            position_value = current_price * quantity
            position_invested = avg_purchase_price * quantity
            position_gain_loss = position_value - position_invested
            
            total_value += position_value
            total_invested += position_invested
            total_gain_loss += position_gain_loss
        
        total_return_pct = (total_gain_loss / total_invested * 100) if total_invested > 0 else 0
        
        return {
            'total_value': round(total_value, 2),
            'total_invested': round(total_invested, 2),
            'total_gain_loss': round(total_gain_loss, 2),
            'total_return_percentage': round(total_return_pct, 2),
            'number_of_positions': len(portfolio_data),
        }
    
    def get_sector_allocation(self, portfolio_data: List[Dict]) -> Dict[str, float]:
        """Calculate portfolio allocation by sector"""
        sector_allocation = {}
        total_value = 0
        
        for position in portfolio_data:
            sector = position.get('sector', 'Unknown')
            value = position.get('current_price', 0) * position.get('quantity', 0)
            
            if sector not in sector_allocation:
                sector_allocation[sector] = 0
            
            sector_allocation[sector] += value
            total_value += value
        
        # Convert to percentages
        if total_value > 0:
            for sector in sector_allocation:
                sector_allocation[sector] = round(sector_allocation[sector] / total_value * 100, 2)
        
        return sector_allocation


# Singleton instances
stock_service = StockDataService()
portfolio_analyzer = PortfolioAnalyzer()
