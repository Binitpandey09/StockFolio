import logging
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.cache import cache_page
from django.db import transaction
from django.utils import timezone

from .models import Stocks, UserInfo, UserStock, Transaction, Watchlist
from .services import stock_service, portfolio_analyzer
import threading

logger = logging.getLogger(__name__)
#

# def fun(request) :
#     page  = '''
#     <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Title</title>
# </head>
# <body>
# <h1>Stock Market App</h1>
# <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Blanditiis commodi dignissimos dolor, ducimus enim harum in ipsum iure laboriosam minus, natus odit officiis omnis optio quibusdam quo, sapiente sunt voluptatibus!</p>
# <ul>
#     <li>s1</li>
#     <li>s2</li>
#     <li>s3</li>
# </ul>
# </body>
# </html>
#     '''
#     return  HttpResponse(page)

@login_required
def index(request):
    user = request.user
    user_stocks = UserStock.objects.select_related('stock').filter(user=user)

    total_value = 0
    invested = 0

    for item in user_stocks:
        stock_value = item.purchase_quantity * item.stock.curr_price
        invested_value = item.purchase_quantity * item.purchase_price

        total_value += stock_value
        invested += invested_value
        item.total_value = stock_value

    gains = ((total_value - invested) / invested) * 100 if invested != 0 else 0

    context = {
        'data': user_stocks,
        'total_value': total_value,
        'invested': invested,
        'gains': round(gains, 2),
    }

    return render(request, 'index.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def populate_stock_data(request):
    """Populate database with stock data using the new service"""
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Only administrators can populate stock data.")
        return redirect('stocks')
    
    nasdaq_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "CRM",
        "PYPL", "INTC", "CSCO", "QCOM", "AVGO", "TXN", "INTU", "AMGN", "BKNG", "GILD"
    ]
    
    success_count = 0
    error_count = 0
    
    try:
        with transaction.atomic():
            for ticker in nasdaq_tickers:
                try:
                    # Check if stock already exists
                    if Stocks.objects.filter(ticker=ticker).exists():
                        logger.info(f"Stock {ticker} already exists, skipping...")
                        continue
                    
                    # Get stock data from service
                    stock_data = stock_service.get_stock_data(ticker)
                    
                    if stock_data:
                        stock = Stocks.objects.create(
                            ticker=stock_data['symbol'],
                            name=stock_data['name'],
                            description=stock_data.get('description', '')[:5000],  # Truncate if too long
                            curr_price=Decimal(str(stock_data['current_price']))
                        )
                        success_count += 1
                        logger.info(f"Successfully added {ticker}: {stock.name}")
                    else:
                        error_count += 1
                        logger.warning(f"Failed to fetch data for {ticker}")
                        
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error processing {ticker}: {str(e)}")
                    continue
            
        message = f"Stock data population completed. Success: {success_count}, Errors: {error_count}"
        if error_count > 0:
            messages.warning(request, message)
        else:
            messages.success(request, message)
            
    except Exception as e:
        logger.error(f"Critical error during stock data population: {str(e)}")
        messages.error(request, "Critical error occurred during stock data population.")
    
    return redirect('stocks')


@login_required
def stocks(request):
    q = request.GET.get('q')
    update_prices = request.GET.get('update_prices', 'false') == 'true'
    
    if q:
        stock_list = Stocks.objects.filter(name__icontains=q).order_by('id') 
    else:
        stock_list = Stocks.objects.all().order_by('id') 

    paginator = Paginator(stock_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Optionally update prices for the current page
    if update_prices:
        try:
            for stock in page_obj:
                stock_data = stock_service.get_stock_data(stock.ticker)
                if stock_data:
                    stock.curr_price = Decimal(str(stock_data['current_price']))
                    stock.volume = stock_data.get('volume', stock.volume)
                    stock.market_cap = stock_data.get('market_cap', stock.market_cap)
                    stock.last_updated = timezone.now()
                    stock.save()
                    logger.info(f"Updated price for {stock.ticker}: ${stock.curr_price}")
        except Exception as e:
            logger.error(f"Error updating stock prices: {str(e)}")
            messages.warning(request, "Some stock prices could not be updated.")
    
    context = {
        'data': page_obj,
        'show_update_button': True,
    }
    return render(request, 'market.html', context)


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logoutView(request) :
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        panCard = request.POST.get('panCard')
        phoneNumber = request.POST.get('phoneNumber')
        profile_pic = request.FILES.get('profile_pic')
        panCard_Image = request.FILES.get('panCard_Image')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        # Check if PAN card is already registered
        if UserInfo.objects.filter(pancard_number=panCard).exists():
            messages.error(request, "PAN card number already registered.")
            return render(request, 'register.html')

        # Create User object
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        # Create UserInfo record
        user_info = UserInfo(
            user=user,
            pancard_number=panCard,
            address=address,
            phone_number=phoneNumber,
            user_image=profile_pic,
            pancard_image=panCard_Image
        )
        user_info.save()

        # Auto login the user
        login(request, user)

        # Send confirmation email asynchronously
        t1 = threading.Thread(
            target=send_email_async,
            kwargs={
                "subject": "Registration Successful",
                "message": f"Dear {user.username}, welcome to our platform!",
                "from_email": None,
                "recipient_list": [user.email],
            }
        )
        t1.start()

        messages.success(request, "Registration successful! Welcome to the platform.")
        return redirect('index')

    return render(request, 'register.html')



@login_required
@require_POST
def buy(request, id):
    """Handle stock purchase with proper validation and error handling"""
    try:
        stock = get_object_or_404(Stocks, id=id)
        user = request.user
        
        # Validate quantity
        try:
            purchase_quantity = int(request.POST.get('quantity', 0))
            if purchase_quantity <= 0:
                messages.error(request, "Quantity must be a positive number.")
                return redirect('stocks')
            
            if purchase_quantity > 10000:  # Reasonable limit
                messages.error(request, "Quantity too large. Maximum allowed is 10,000 shares.")
                return redirect('stocks')
                
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity provided.")
            return redirect('stocks')
        
        # Get current stock price (update from live data if possible)
        current_data = stock_service.get_stock_data(stock.ticker)
        if current_data:
            purchase_price = Decimal(str(current_data['current_price']))
            # Update stock price in database
            stock.curr_price = purchase_price
            stock.save()
        else:
            purchase_price = stock.curr_price
            logger.warning(f"Could not fetch live price for {stock.ticker}, using stored price")
        
        # Calculate total cost
        total_cost = purchase_price * purchase_quantity
        
        with transaction.atomic():
            # Update or create user stock position
            user_stock, created = UserStock.objects.get_or_create(
                user=user,
                stock=stock,
                defaults={
                    'purchase_price': purchase_price,
                    'purchase_quantity': purchase_quantity
                }
            )
            
            if not created:
                # Calculate weighted average price
                total_quantity = user_stock.purchase_quantity + purchase_quantity
                total_value = (user_stock.purchase_quantity * user_stock.purchase_price + 
                             purchase_quantity * purchase_price)
                user_stock.purchase_price = total_value / total_quantity
                user_stock.purchase_quantity = total_quantity
                user_stock.save()
            
            # Record transaction
            Transaction.objects.create(
                user=user,
                stock_symbol=stock.ticker,
                stock_name=stock.name,
                quantity=purchase_quantity,
                price=purchase_price,
                type='BUY'
            )
            
        # Send email notification asynchronously
        try:
            email_thread = threading.Thread(
                target=send_email_async,
                kwargs={
                    "subject": "Stock Purchase Confirmation",
                    "message": f"You successfully purchased {purchase_quantity} shares of {stock.name} at ${purchase_price:.2f} per share. Total: ${total_cost:.2f}",
                    "from_email": None,
                    "recipient_list": [user.email],
                }
            )
            email_thread.daemon = True
            email_thread.start()
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
        
        messages.success(request, f"Successfully purchased {purchase_quantity} shares of {stock.name} for ${total_cost:.2f}")
        logger.info(f"User {user.username} bought {purchase_quantity} shares of {stock.ticker} at ${purchase_price}")
        
    except Exception as e:
        logger.error(f"Error in buy transaction for user {request.user.username}: {str(e)}")
        messages.error(request, "An error occurred during the purchase. Please try again.")
    
    return redirect('index')



def  sell(request , id) :
    stock = get_object_or_404(Stocks, id=id)
    user = request.user
    sell_quantity = int(request.POST.get('quantity'))
    userStock  =  UserStock.objects.filter(stock  =  stock ,  user =  user).first()

    if userStock.purchase_quantity <  sell_quantity :
        messages.error(request, "Can't sell more than you own")
        return redirect('market')

    userStock.purchase_quantity -= sell_quantity
    userStock.save()

    Transaction.objects.create(
        user=user,
        stock_symbol=stock.ticker,
        stock_name=stock.name,
        quantity=sell_quantity,
        price=stock.curr_price,
        type='SELL'
    )

    t1 = threading.Thread(
        target=send_email_async,
        kwargs={
            "subject": "Sell Option executed successfully",
            "message": f"Your sale of stock {stock.name} was successful",
            "from_email": None,
            "recipient_list": [user.email],
        }
    )
    t1.start()

    return redirect('index')




def send_email_async(subject  ,  message  ,  from_email , recipient_list ) :
    send_mail(subject  =  subject ,  message =  message ,  from_email= from_email , recipient_list = recipient_list )



@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    context = {
        "transactions": transactions
    }
    return render(request, "transaction_history.html", context)




@login_required
def portfolio_dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    portfolio = {}
    for t in transactions:
        if t.stock_symbol not in portfolio:
            portfolio[t.stock_symbol] = {
                'stock_name': t.stock_name,
                'quantity': 0,
                'invested_value': 0.0,
                'current_price': 0.0, # This will be updated if live prices are integrated
            }
        if t.type == 'BUY':
            portfolio[t.stock_symbol]['quantity'] += t.quantity
            portfolio[t.stock_symbol]['invested_value'] += float(t.quantity * t.price)
        elif t.type == 'SELL':
            portfolio[t.stock_symbol]['quantity'] -= t.quantity
            portfolio[t.stock_symbol]['invested_value'] -= float(t.quantity * t.price) # This might need more sophisticated calculation for average cost

    # Remove stocks with zero quantity (if any after buy/sell)
    portfolio = {symbol: data for symbol, data in portfolio.items() if data['quantity'] > 0}

    # Get current live prices for portfolio stocks
    for symbol, data in portfolio.items():
        try:
            # Get live price data
            stock_data = stock_service.get_stock_data(symbol)
            if stock_data:
                data['current_price'] = stock_data['current_price']
                data['day_change'] = stock_data.get('day_change', 0)
                data['day_change_percent'] = stock_data.get('day_change_percent', 0)
                data['sector'] = stock_data.get('sector', 'N/A')
                
                # Update database price
                stock = Stocks.objects.filter(ticker=symbol).first()
                if stock:
                    stock.curr_price = Decimal(str(stock_data['current_price']))
                    stock.last_updated = timezone.now()
                    stock.save()
            else:
                # Fallback to database price
                stock = Stocks.objects.filter(ticker=symbol).first()
                data['current_price'] = float(stock.curr_price) if stock else 0.0
                data['day_change'] = 0
                data['day_change_percent'] = 0
                data['sector'] = stock.sector if stock else 'N/A'
        except Exception as e:
            logger.error(f"Error fetching live price for {symbol}: {str(e)}")
            # Use database price as fallback
            stock = Stocks.objects.filter(ticker=symbol).first()
            data['current_price'] = float(stock.curr_price) if stock else 0.0
            data['day_change'] = 0
            data['day_change_percent'] = 0
            data['sector'] = stock.sector if stock else 'N/A'
            
        data['current_value'] = data['quantity'] * data['current_price']
        data['gain_loss'] = data['current_value'] - data['invested_value']
        data['gain_loss_percent'] = (data['gain_loss'] / data['invested_value']) * 100 if data['invested_value'] > 0 else 0

    total_portfolio_value = sum(item['current_value'] for item in portfolio.values())
    total_invested_capital = sum(item['invested_value'] for item in portfolio.values())

    context = {
        'portfolio': portfolio,
        'total_portfolio_value': total_portfolio_value,
        'total_invested_capital': total_invested_capital,
    }
    return render(request, 'portfolio_dashboard.html', context)


@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    
    # Enhance watchlist items with current prices and additional data
    enhanced_watchlist = []
    for item in watchlist_items:
        try:
            # Get the stock from database
            stock = Stocks.objects.filter(ticker=item.stock_symbol).first()
            
            # Get live price data
            stock_data = stock_service.get_stock_data(item.stock_symbol)
            
            if stock_data:
                # Update stock price in database if we got live data
                if stock:
                    stock.curr_price = Decimal(str(stock_data['current_price']))
                    stock.last_updated = timezone.now()
                    stock.save()
                
                enhanced_item = {
                    'id': item.id,
                    'stock_symbol': item.stock_symbol,
                    'stock_name': item.stock_name,
                    'current_price': stock_data['current_price'],
                    'previous_close': stock_data.get('previous_close', stock_data['current_price']),
                    'day_change': stock_data.get('day_change', 0),
                    'day_change_percent': stock_data.get('day_change_percent', 0),
                    'volume': stock_data.get('volume', 0),
                    'market_cap': stock_data.get('market_cap', 0),
                    'sector': stock_data.get('sector', 'N/A'),
                    'source': stock_data.get('source', 'API')
                }
            else:
                # Fallback to stored data if live data is not available
                enhanced_item = {
                    'id': item.id,
                    'stock_symbol': item.stock_symbol,
                    'stock_name': item.stock_name,
                    'current_price': float(stock.curr_price) if stock else 0.0,
                    'previous_close': float(stock.curr_price) if stock else 0.0,
                    'day_change': 0,
                    'day_change_percent': 0,
                    'volume': stock.volume if stock else 0,
                    'market_cap': stock.market_cap if stock else 0,
                    'sector': stock.sector if stock else 'N/A',
                    'source': 'Database (Offline)'
                }
            
            enhanced_watchlist.append(enhanced_item)
            
        except Exception as e:
            logger.error(f"Error fetching data for watchlist item {item.stock_symbol}: {str(e)}")
            # Add basic item even if there's an error
            enhanced_watchlist.append({
                'id': item.id,
                'stock_symbol': item.stock_symbol,
                'stock_name': item.stock_name,
                'current_price': 0.0,
                'previous_close': 0.0,
                'day_change': 0,
                'day_change_percent': 0,
                'volume': 0,
                'market_cap': 0,
                'sector': 'Error',
                'source': 'Error'
            })
    
    context = {
        "watchlist_items": enhanced_watchlist,
        "total_items": len(enhanced_watchlist)
    }
    return render(request, "watchlist.html", context)

@login_required
def add_to_watchlist(request, stock_symbol):
    stock = get_object_or_404(Stocks, ticker=stock_symbol)
    Watchlist.objects.get_or_create(user=request.user, stock_symbol=stock.ticker, stock_name=stock.name)
    messages.success(request, f"{stock.name} added to watchlist.")
    return redirect("stocks")

@login_required
def remove_from_watchlist(request, stock_symbol):
    stock = get_object_or_404(Stocks, ticker=stock_symbol)
    Watchlist.objects.filter(user=request.user, stock_symbol=stock.ticker).delete()
    messages.success(request, f"{stock.name} removed from watchlist.")
    return redirect("watchlist_view")


@login_required
def get_stock_price_api(request, symbol):
    """API endpoint to get real-time stock price data"""
    try:
        stock_data = stock_service.get_stock_data(symbol.upper())
        
        if stock_data:
            # Update database
            stock = Stocks.objects.filter(ticker=symbol.upper()).first()
            if stock:
                stock.curr_price = Decimal(str(stock_data['current_price']))
                stock.last_updated = timezone.now()
                stock.save()
            
            return JsonResponse({
                'success': True,
                'symbol': stock_data['symbol'],
                'current_price': stock_data['current_price'],
                'previous_close': stock_data.get('previous_close', stock_data['current_price']),
                'day_change': stock_data.get('day_change', 0),
                'day_change_percent': stock_data.get('day_change_percent', 0),
                'volume': stock_data.get('volume', 0),
                'market_cap': stock_data.get('market_cap', 0),
                'last_updated': timezone.now().isoformat(),
                'source': stock_data.get('source', 'API')
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Could not fetch stock data',
                'symbol': symbol.upper()
            }, status=404)
            
    except Exception as e:
        logger.error(f"API error for {symbol}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'symbol': symbol.upper()
        }, status=500)


@login_required
def update_watchlist_prices_api(request):
    """API endpoint to update all watchlist prices at once"""
    try:
        watchlist_items = Watchlist.objects.filter(user=request.user)
        updated_prices = []
        errors = []
        
        for item in watchlist_items:
            try:
                stock_data = stock_service.get_stock_data(item.stock_symbol)
                if stock_data:
                    # Update database
                    stock = Stocks.objects.filter(ticker=item.stock_symbol).first()
                    if stock:
                        stock.curr_price = Decimal(str(stock_data['current_price']))
                        stock.last_updated = timezone.now()
                        stock.save()
                    
                    updated_prices.append({
                        'symbol': stock_data['symbol'],
                        'current_price': stock_data['current_price'],
                        'day_change': stock_data.get('day_change', 0),
                        'day_change_percent': stock_data.get('day_change_percent', 0),
                        'volume': stock_data.get('volume', 0)
                    })
                else:
                    errors.append(f"Could not fetch data for {item.stock_symbol}")
            except Exception as e:
                errors.append(f"Error updating {item.stock_symbol}: {str(e)}")
        
        return JsonResponse({
            'success': True,
            'updated_count': len(updated_prices),
            'error_count': len(errors),
            'prices': updated_prices,
            'errors': errors,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Watchlist API error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


