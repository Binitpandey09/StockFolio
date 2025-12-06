# StockFolio Features Guide

## 📊 Complete Feature List

### 1. User Authentication & Profile
- **User Registration**
  - Username, email, password
  - Profile information (phone, address, PAN card)
  - Profile picture upload
  - PAN card image upload
  - Email verification

- **Login/Logout**
  - Secure authentication
  - Session management
  - Remember me functionality

- **User Preferences** ⭐ NEW
  - Email notification settings
  - Price alert notifications
  - Transaction notifications
  - Theme selection (Light/Dark)
  - Account information view

### 2. Stock Market Data
- **Real-Time Prices**
  - Live stock prices from yfinance API
  - 72+ major stocks (AAPL, MSFT, GOOGL, TSLA, etc.)
  - Auto-refresh capability
  - Price caching (5-minute cache)

- **Stock Information**
  - Current price
  - Market capitalization
  - Trading volume
  - Sector and industry
  - Day change and percentage
  - Previous close price

- **Stock Search**
  - Search by ticker symbol
  - Search by company name
  - Real-time search results
  - Pagination support

### 3. Trading Features
- **Buy Stocks**
  - Purchase at current market price
  - Quantity validation
  - Weighted average price calculation
  - Transaction recording
  - Email confirmation

- **Sell Stocks**
  - Sell owned stocks
  - Quantity validation (can't sell more than owned)
  - Profit/Loss calculation
  - Transaction recording
  - Email confirmation

- **Transaction History**
  - Complete trade history
  - Buy/Sell records
  - Date, quantity, price details
  - Sortable and filterable
  - Export capability

### 4. Portfolio Management
- **Portfolio Dashboard**
  - All owned stocks display
  - Current value vs invested value
  - Individual stock performance
  - Total portfolio value
  - Gain/Loss calculations
  - Real-time updates

- **Analytics Dashboard** ⭐ NEW
  - Comprehensive portfolio metrics
  - Summary statistics cards
  - Detailed breakdown table
  - Performance indicators
  - Quick action buttons
  - Holdings count

### 5. Watchlist
- **Add to Watchlist**
  - Monitor stocks without buying
  - Quick add from market page
  - Unlimited watchlist items

- **Watchlist View**
  - Live price updates
  - Day change indicators
  - Volume and market cap
  - Sector information
  - Remove from watchlist
  - Quick buy action

### 6. Price Alerts ⭐ NEW
- **Create Alerts**
  - Set target prices
  - Alert types: Above/Below
  - Multiple alerts per stock
  - Custom alert names

- **Alert Management**
  - View all alerts
  - Active/Triggered status
  - Current price comparison
  - Delete alerts
  - Alert history

- **Notifications**
  - Email notifications
  - Real-time alert checking
  - Triggered alert tracking

### 7. Stock Comparison ⭐ NEW
- **Compare Stocks**
  - Compare up to 5 stocks
  - Side-by-side comparison
  - Key metrics display
  - Real-time data

- **Comparison Metrics**
  - Current price
  - Day change & percentage
  - Volume
  - Market capitalization
  - Sector
  - P/E ratio (when available)

- **Save Comparisons**
  - Name your comparisons
  - Load saved comparisons
  - Comparison history
  - Quick access

### 8. Admin Features
- **Stock Management**
  - Add/Edit/Delete stocks
  - Bulk stock import
  - Price updates
  - Stock activation/deactivation

- **User Management**
  - View all users
  - User profiles
  - Transaction history
  - Portfolio overview

- **System Management**
  - Database management
  - Log viewing
  - System health checks
  - API monitoring

### 9. API Endpoints
- **Stock Data API**
  - `/api/stock/<symbol>/price/` - Get real-time price
  - `/api/stock/search/` - Search stocks
  - `/api/watchlist/update-prices/` - Update watchlist

- **Health Checks**
  - `/api/health/` - System health
  - `/api/ready/` - Readiness check
  - `/api/alive/` - Liveness check

### 10. Email Notifications
- **Registration**
  - Welcome email
  - Account confirmation

- **Trading**
  - Buy confirmation
  - Sell confirmation
  - Transaction details

- **Alerts**
  - Price alert triggered
  - Target price reached

### 11. User Interface
- **Modern Design**
  - Bootstrap 5 framework
  - Responsive layout
  - Mobile-friendly
  - Gradient colors

- **Navigation**
  - Intuitive menu structure
  - Dropdown menus
  - Quick access links
  - User profile dropdown

- **Visual Elements**
  - Card-based layout
  - Hover effects
  - Smooth transitions
  - Custom scrollbar
  - Loading indicators

### 12. Security Features
- **Authentication**
  - Password hashing
  - Session management
  - CSRF protection
  - XSS prevention

- **Data Protection**
  - Secure forms
  - Input validation
  - SQL injection prevention
  - Rate limiting

### 13. Performance
- **Caching**
  - Stock price caching
  - Query optimization
  - Static file compression

- **Optimization**
  - Database indexing
  - Lazy loading
  - Pagination
  - Async operations

---

## 🎯 How to Use Key Features

### Setting Up Price Alerts
1. Navigate to "Alerts" in the menu
2. Enter stock symbol (e.g., AAPL)
3. Choose alert type (Above/Below)
4. Set target price
5. Click "Create Alert"
6. Receive email when triggered

### Comparing Stocks
1. Go to "Compare" in the menu
2. Enter up to 5 stock symbols
3. Click "Compare"
4. View side-by-side metrics
5. Save comparison for later

### Managing Your Portfolio
1. View "Analytics" dashboard
2. See all holdings and performance
3. Check gain/loss for each stock
4. Use quick actions to trade
5. Monitor total portfolio value

### Using Watchlist
1. Browse stocks in "Market"
2. Click "Add to Watchlist"
3. View watchlist for monitoring
4. Get real-time price updates
5. Quick buy from watchlist

---

**Need Help?** Contact support or check the documentation.

**Developed by:** Binit Pandey  
**Version:** 2.0
