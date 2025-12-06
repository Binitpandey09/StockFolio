# 📈 StockFolio

**Smart Stock Trading Simulation Platform**

A comprehensive real-time stock trading simulation platform built with Django. Practice trading with real market data without risking real money. Perfect for learning stock market trading and portfolio management.

**Developed by:** Binit Pandey  
**Version:** 2.0  
**License:** MIT

## 🎯 Core Features

### 📊 Trading & Portfolio
- **Real-Time Stock Data** - Live prices from 72+ major stocks (AAPL, MSFT, GOOGL, TSLA, etc.)
- **Buy/Sell Stocks** - Execute trades at current market prices
- **Portfolio Management** - Track your investments with real-time valuations
- **Transaction History** - Complete record of all your trades
- **Analytics Dashboard** - Comprehensive portfolio performance metrics

### 🔔 Advanced Features (NEW)
- **Price Alerts** - Set custom price alerts for any stock (above/below target price)
- **Stock Comparison** - Compare multiple stocks side-by-side with key metrics
- **Watchlist** - Monitor stocks you're interested in with live updates
- **User Preferences** - Customize notifications and app settings
- **Email Notifications** - Get notified about trades, alerts, and important updates

### 💼 Portfolio Analytics
- Total portfolio value tracking
- Gain/Loss calculations ($ and %)
- Individual stock performance
- Sector allocation
- Investment returns analysis

### 🎨 User Experience
- Modern, responsive design
- Bootstrap 5 UI
- Mobile-friendly interface
- Real-time price updates
- Search functionality
- Intuitive navigation

🚀 Quick Setup & Run
Prerequisites

Python 3.11+ installed

pip (Python package manager)

Easy Setup

Install dependencies:

pip install -r requirements.txt


Run database migrations:
python manage.py migrate


Create admin user:
python manage.py createsuperuser


Populate with stock data:
python manage.py populate_stocks


Start the application:
python manage.py runserver

Your application will be live at http://localhost:8000

🌐 Access Your Application
Main Application → http://localhost:8000
Admin Panel → http://localhost:8000/admin
API Health Check → http://localhost:8000/api/health/

✔ Use the superuser credentials created earlier.

💼 Using the Application
Register/Login
Browse stocks
Add stocks to watchlist
Perform simulated trades
Track your portfolio
Check transaction history

🏗️ Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django App    │    │   Stock APIs    │
│   (HTML/CSS/JS) │◄──►│   (Python)      │◄──►│   (yfinance)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite/PG)   │
                       └─────────────────┘

📊 Available Stocks
Tech: AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA, NFLX
Finance: JPM, BAC, WFC, GS, MS, V, MA, AXP
Healthcare: JNJ, PFE, UNH, MRK, ABT, ABBV
Consumer Goods: KO, PEP, WMT, COST, MCD, NKE
ETFs: SPY, QQQ, IWM, VTI

Total 72+ real market stocks

🔧 Development
Local Development (without Docker)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_stocks
python manage.py runserver

Additional Commands
python manage.py populate_stocks --symbols AAPL MSFT GOOGL
python manage.py runserver --verbosity=2
python manage.py runserver 0.0.0.0:8080

🔗 API Endpoints

/api/stock/<symbol>/price/

/api/watchlist/update-prices/

/api/health/

/api/ready/

/api/alive/

🛠️ Tech Stack

Backend: Django 4.2

Language: Python 3.11+

Frontend: HTML, CSS, JavaScript, Bootstrap

Database: SQLite

Stock Data: yfinance

Caching: In-memory

📝 License

This project is open source and available under the MIT License.

🤝 Contributing

Fork

Create feature branch

Commit changes

Submit PR

🆘 Support

If you face issues:

pip install -r requirements.txt

python manage.py migrate

python manage.py populate_stocks

Check terminal logs

## 🆕 What's New in Version 2.0

### Enhanced Features
✅ **Price Alerts System** - Never miss a price target  
✅ **Stock Comparison Tool** - Compare up to 5 stocks simultaneously  
✅ **Advanced Analytics Dashboard** - Detailed portfolio insights  
✅ **User Preferences** - Customizable notifications and settings  
✅ **Improved UI/UX** - Modern Bootstrap 5 design  
✅ **Better Navigation** - Intuitive menu structure  
✅ **Enhanced Admin Panel** - Better stock and user management  

### Removed
❌ Docker/Ansible/Nagios setup (simplified deployment)

---

## 📸 Screenshots

### Dashboard
View your complete portfolio with real-time valuations and performance metrics.

### Market
Browse 72+ stocks with live prices, search functionality, and quick actions.

### Price Alerts
Set custom alerts and get notified when stocks hit your target prices.

### Stock Comparison
Compare multiple stocks side-by-side with key financial metrics.

---

Happy Trading! 📈💰







