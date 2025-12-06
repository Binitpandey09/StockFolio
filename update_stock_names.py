"""
Update stock names in the database
You can customize stock names to be more descriptive
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from stocks.models import Stocks
from stocks.services import stock_service

def update_single_stock(ticker, new_name=None):
    """Update a single stock's name"""
    try:
        stock = Stocks.objects.get(ticker=ticker.upper())
        old_name = stock.name
        
        if new_name:
            # Use custom name
            stock.name = new_name
            stock.save()
            print(f"✅ {ticker}: Updated")
            print(f"   Old: {old_name}")
            print(f"   New: {new_name}\n")
        else:
            # Fetch fresh name from Yahoo Finance
            print(f"🔍 Fetching fresh data for {ticker}...")
            stock_data = stock_service.get_stock_data(ticker, use_cache=False)
            
            if stock_data:
                stock.name = stock_data['name'][:300]
                stock.save()
                print(f"✅ {ticker}: Updated from Yahoo Finance")
                print(f"   Old: {old_name}")
                print(f"   New: {stock.name}\n")
            else:
                print(f"❌ {ticker}: Failed to fetch data\n")
        
        return True
    except Stocks.DoesNotExist:
        print(f"❌ {ticker}: Stock not found in database\n")
        return False

def update_all_stocks():
    """Refresh all stock names from Yahoo Finance"""
    print("\n" + "="*70)
    print("REFRESHING ALL STOCK NAMES FROM YAHOO FINANCE")
    print("="*70 + "\n")
    
    stocks = Stocks.objects.all()
    success_count = 0
    
    for stock in stocks:
        print(f"Processing {stock.ticker}...")
        stock_data = stock_service.get_stock_data(stock.ticker, use_cache=False)
        
        if stock_data:
            old_name = stock.name
            new_name = stock_data['name'][:300]
            
            if old_name != new_name:
                stock.name = new_name
                stock.save()
                print(f"  ✅ Updated: {old_name} → {new_name}")
                success_count += 1
            else:
                print(f"  ✓ No change needed")
        else:
            print(f"  ❌ Failed to fetch data")
    
    print(f"\n{'='*70}")
    print(f"Updated {success_count} stock names")
    print(f"{'='*70}\n")

def show_custom_name_examples():
    """Show examples of custom names you might want"""
    print("\n" + "="*70)
    print("CUSTOM NAME EXAMPLES")
    print("="*70 + "\n")
    
    examples = {
        'AAPL': 'Apple Inc. - iPhone, Mac, iPad Maker',
        'GOOGL': 'Alphabet Inc. - Google Parent Company',
        'AMZN': 'Amazon.com, Inc. - E-commerce & Cloud Giant',
        'TSLA': 'Tesla, Inc. - Electric Vehicle Manufacturer',
        'META': 'Meta Platforms, Inc. - Facebook, Instagram, WhatsApp',
        'MSFT': 'Microsoft Corporation - Windows, Office, Azure',
        'NVDA': 'NVIDIA Corporation - Graphics & AI Chips',
    }
    
    print("You can make names more descriptive like this:\n")
    for ticker, custom_name in examples.items():
        try:
            stock = Stocks.objects.get(ticker=ticker)
            print(f"{ticker:8} | Current: {stock.name}")
            print(f"         | Custom:  {custom_name}\n")
        except Stocks.DoesNotExist:
            pass
    
    print("="*70 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("STOCK NAME UPDATE TOOL")
        print("="*70)
        print("\nUsage:")
        print("  1. Update single stock with custom name:")
        print("     python update_stock_names.py AAPL 'Apple Inc. - Technology Giant'")
        print("\n  2. Refresh single stock from Yahoo Finance:")
        print("     python update_stock_names.py AAPL")
        print("\n  3. Refresh all stocks from Yahoo Finance:")
        print("     python update_stock_names.py --all")
        print("\n  4. Show custom name examples:")
        print("     python update_stock_names.py --examples")
        print("="*70 + "\n")
        sys.exit(0)
    
    if sys.argv[1] == '--all':
        update_all_stocks()
    elif sys.argv[1] == '--examples':
        show_custom_name_examples()
    elif len(sys.argv) == 3:
        # Update with custom name
        ticker = sys.argv[1]
        custom_name = sys.argv[2]
        update_single_stock(ticker, custom_name)
    else:
        # Refresh from Yahoo Finance
        ticker = sys.argv[1]
        update_single_stock(ticker)
