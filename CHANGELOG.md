# StockFolio Changelog

## Version 2.0 - December 7, 2025

### 🎉 Major Enhancements

#### New Features Added
1. **Price Alerts System**
   - Set custom price alerts for any stock
   - Alert types: Price Above / Price Below
   - Real-time alert monitoring
   - Email notifications when alerts trigger
   - Alert status tracking (Active/Triggered/Cancelled)

2. **Stock Comparison Tool**
   - Compare up to 5 stocks side-by-side
   - Key metrics comparison:
     - Current price
     - Day change & percentage
     - Volume
     - Market cap
     - Sector information
   - Save and load comparisons
   - Quick comparison from market page

3. **Advanced Analytics Dashboard**
   - Comprehensive portfolio overview
   - Real-time portfolio valuation
   - Individual stock performance tracking
   - Gain/Loss calculations ($ and %)
   - Quick action buttons
   - Summary statistics cards

4. **User Preferences**
   - Customizable notification settings
   - Email notification controls
   - Price alert notification toggle
   - Transaction notification settings
   - Theme selection (Light/Dark)
   - Account information display

5. **Enhanced UI/UX**
   - Modern Bootstrap 5 design
   - Improved navigation with dropdown menus
   - Better footer with multiple sections
   - Enhanced card designs with hover effects
   - Gradient buttons and backgrounds
   - Responsive design improvements
   - Custom scrollbar styling

#### Improvements
- **Admin Panel**: Enhanced with better list displays, filters, and search
- **Navigation**: Reorganized menu with better categorization
- **Branding**: Updated to "StockFolio" throughout the application
- **Footer**: Comprehensive footer with links and developer credit
- **Models**: Added new models for alerts, comparisons, and preferences
- **API Endpoints**: New endpoints for stock search and enhanced data

#### Removed
- Docker setup (infra/ansible/)
- Ansible configuration files
- Nagios monitoring setup
- All DevOps infrastructure files

### 🔧 Technical Changes

#### Database Models
- Added `PriceAlert` model
- Added `StockComparison` model
- Added `UserPreference` model
- Enhanced `Watchlist` model with `added_at` field

#### New Files
- `stocks/enhanced_views.py` - New feature views
- `stocks/templates/price_alerts.html`
- `stocks/templates/stock_comparison.html`
- `stocks/templates/user_preferences.html`
- `stocks/templates/dashboard_analytics.html`
- `stocks/static/enhanced-styles.css`
- `CHANGELOG.md`

#### Modified Files
- `stocks/models.py` - Added new models
- `stocks/admin.py` - Enhanced admin interface
- `stocks/urls.py` - Added new URL patterns
- `stocks/templates/base.html` - Updated title and styles
- `stocks/templates/components/navbar.html` - Complete redesign
- `stocks/templates/components/footer.html` - Enhanced footer
- `README.md` - Updated documentation

#### Migrations
- `0007_watchlist_added_at_userpreference_stockcomparison_and_more.py`

### 🎨 Design Changes
- New color scheme with gradients
- Enhanced card shadows and hover effects
- Better button styling
- Improved form controls
- Custom scrollbar
- Responsive footer design

### 👤 Branding
- Changed from "Investing.com" to "StockFolio"
- Added developer credit: Binit Pandey
- Updated all references throughout the application

### 📝 Documentation
- Updated README with new features
- Added version information
- Removed Docker/Ansible documentation
- Added feature highlights

---

## Version 1.0 - Initial Release

### Features
- Real-time stock data from yfinance
- Buy/Sell stock functionality
- Portfolio management
- Transaction history
- Watchlist
- Email notifications
- Admin dashboard
- User authentication
- Stock price updates

---

**Developed by:** Binit Pandey  
**Repository:** https://github.com/Binitpandey09/StockFolio  
**License:** MIT
