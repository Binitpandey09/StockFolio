"""
Django management command to populate the database with real stock data.
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from stocks.models import Stocks
from stocks.services import stock_service
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate database with popular stock data using real-time APIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--symbols',
            nargs='+',
            type=str,
            help='Specific stock symbols to add (e.g., AAPL MSFT GOOGL)',
            default=None
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing stocks before adding new ones',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Number of stocks to process in each batch',
        )

    def handle(self, *args, **options):
        """Main command handler"""
        
        if options['clear']:
            self.stdout.write('Clearing existing stock data...')
            deleted_count = Stocks.objects.all().delete()[0]
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {deleted_count} existing stocks')
            )

        # Default popular stocks if no symbols provided
        default_symbols = [
            # Tech Giants
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX',
            # Other Popular Stocks
            'JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'MA', 'DIS',
            'ADBE', 'CRM', 'PYPL', 'INTC', 'CSCO', 'PFE', 'VZ', 'T',
            'KO', 'PEP', 'WMT', 'MRK', 'ABT', 'TMO', 'COST', 'AVGO',
            # Financial
            'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP',
            # Healthcare
            'JNJ', 'UNH', 'PFE', 'ABBV', 'MRK', 'TMO',
            # Energy
            'XOM', 'CVX', 'COP', 'SLB',
            # Consumer
            'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX'
        ]
        
        symbols_to_process = options['symbols'] or default_symbols
        # Remove duplicates and convert to uppercase
        symbols_to_process = list(set(symbol.upper() for symbol in symbols_to_process))
        
        self.stdout.write(f'Processing {len(symbols_to_process)} stock symbols...')
        
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        batch_size = options['batch_size']
        
        for i in range(0, len(symbols_to_process), batch_size):
            batch = symbols_to_process[i:i + batch_size]
            self.stdout.write(f'Processing batch {i//batch_size + 1}: {", ".join(batch)}')
            
            try:
                with transaction.atomic():
                    for symbol in batch:
                        try:
                            # Check if stock already exists
                            if Stocks.objects.filter(ticker=symbol).exists():
                                self.stdout.write(
                                    self.style.WARNING(f'  {symbol}: Already exists, skipping')
                                )
                                skipped_count += 1
                                continue
                            
                            # Fetch stock data
                            stock_data = stock_service.get_stock_data(symbol)
                            
                            if stock_data:
                                # Create stock record
                                stock = Stocks.objects.create(
                                    ticker=stock_data['symbol'],
                                    name=stock_data['name'][:300],  # Ensure it fits
                                    description=stock_data.get('description', '')[:5000],
                                    curr_price=Decimal(str(stock_data['current_price'])),
                                    market_cap=stock_data.get('market_cap'),
                                    sector=stock_data.get('sector', '')[:100],
                                    industry=stock_data.get('industry', '')[:100],
                                    volume=stock_data.get('volume', 0),
                                    is_active=True
                                )
                                
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  ✓ {symbol}: {stock.name} - ${stock.curr_price}'
                                    )
                                )
                                success_count += 1
                                
                            else:
                                self.stdout.write(
                                    self.style.ERROR(f'  ✗ {symbol}: Failed to fetch data')
                                )
                                error_count += 1
                                
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'  ✗ {symbol}: Error - {str(e)}')
                            )
                            error_count += 1
                            logger.error(f'Error processing {symbol}: {str(e)}')
                            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Batch processing error: {str(e)}')
                )
                error_count += len(batch)
        
        # Summary
        total_processed = success_count + error_count + skipped_count
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SUMMARY:')
        self.stdout.write(f'Total symbols processed: {total_processed}')
        self.stdout.write(self.style.SUCCESS(f'Successfully added: {success_count}'))
        self.stdout.write(self.style.WARNING(f'Skipped (already exist): {skipped_count}'))
        self.stdout.write(self.style.ERROR(f'Failed: {error_count}'))
        self.stdout.write(f'Database now contains: {Stocks.objects.count()} total stocks')
        
        if success_count > 0:
            self.stdout.write('\nSample of added stocks:')
            for stock in Stocks.objects.order_by('-created_at')[:5]:
                self.stdout.write(f'  {stock.ticker}: {stock.name} - ${stock.curr_price}')
        
        self.stdout.write('\n' + self.style.SUCCESS('Stock population completed!'))
        
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\nNote: {error_count} stocks failed to load. '
                    'This might be due to API rate limits or invalid symbols. '
                    'You can run the command again to retry failed stocks.'
                )
            )
