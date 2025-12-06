"""
Easy Stock Addition Script for StockFolio
Run this script to easily add stocks to your database
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from stocks.models import Stocks
from stocks.services import stock_service
from decimal import Decimal

def show_current_stocks():
    """Display current stocks in database"""
    stocks = Stocks.objects.all().order_by('ticker')
    print(f"\n{'='*70}")
    print(f"CURRENT STOCKS IN DATABASE: {stocks.count()}")
    print(f"{'='*70}")
    for stock in stocks:
        print(f"  {stock.ticker:8} - {stock.name}")
    print(f"{'='*70}\n")

def add_stock(symbol):
    """Add a single stock to database"""
    symbol = symbol.upper().strip()
    
    # Check if already exists
    if Stocks.objects.filter(ticker=symbol).exists():
        print(f"❌ {symbol} already exists in database!")
        return False
    
    # Fetch stock data
    print(f"🔍 Fetching data for {symbol}...")
    stock_data = stock_service.get_stock_data(symbol, use_cache=False)
    
    if not stock_data:
        print(f"❌ Failed to fetch data for {symbol}. Invalid symbol or API error.")
        return False
    
    # Create stock record
    try:
        stock = Stocks.objects.create(
            ticker=stock_data['symbol'],
            name=stock_data['name'][:300],
            description=stock_data.get('description', '')[:5000],
            curr_price=Decimal(str(stock_data['current_price'])),
            market_cap=stock_data.get('market_cap'),
            sector=stock_data.get('sector', '')[:100],
            industry=stock_data.get('industry', '')[:100],
            volume=stock_data.get('volume', 0),
            is_active=True
        )
        print(f"✅ Successfully added: {stock.ticker} - {stock.name} (${stock.curr_price})")
        return True
    except Exception as e:
        print(f"❌ Error adding {symbol}: {str(e)}")
        return False

def main():
    """Main function"""
    print("\n" + "="*70)
    print("  STOCKFOLIO - EASY STOCK ADDITION TOOL")
    print("="*70)
    
    show_current_stocks()
    
    print("📝 POPULAR STOCK CATEGORIES:")
    print("\n1. Tech Giants:")
    print("   AAPL MSFT GOOGL AMZN META NVDA TSLA NFLX ADBE CRM")
    print("\n2. Finance:")
    print("   JPM BAC WFC GS MS C V MA AXP BLK")
    print("\n3. Healthcare:")
    print("   JNJ UNH PFE ABBV MRK TMO LLY ABT")
    print("\n4. Energy:")
    print("   XOM CVX COP SLB")
    print("\n5. Retail:")
    print("   WMT TGT COST HD LOW MCD SBUX NKE")
    
    print("\n" + "="*70)
    print("Enter stock symbols separated by spaces (or 'quit' to exit)")
    print("Example: AAPL MSFT GOOGL")
    print("="*70 + "\n")
    
    while True:
        user_input = input("Enter stock symbols: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Split symbols
        symbols = user_input.upper().split()
        
        print(f"\n📊 Adding {len(symbols)} stock(s)...\n")
        
        success_count = 0
        for symbol in symbols:
            if add_stock(symbol):
                success_count += 1
        
        print(f"\n✨ Summary: {success_count}/{len(symbols)} stocks added successfully!")
        print(f"📈 Total stocks in database: {Stocks.objects.count()}\n")
        
        continue_choice = input("Add more stocks? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
