from django.core.management.base import BaseCommand
from apps.market_data.services import run_pipeline_for_ticker


class Command(BaseCommand):
    help = 'Runs the market data pipeline for one or all tickers'

    def add_arguments(self, parser):
        parser.add_argument('--ticker', type=str, help='Single ticker to process (e.g. AAPL)')
        parser.add_argument('--skip-fundamentals', action='store_true', help='Skip fundamentals fetch')

    def handle(self, *args, **options):
        ticker = options.get('ticker')

        if ticker:
            tickers = [ticker.upper()]
        else:
            from apps.market_data.models import Asset
            tickers = list(Asset.objects.values_list('ticker', flat=True))

        if not tickers:
            self.stdout.write(self.style.WARNING('No tickers found. Add assets first via /admin.'))
            return

        for t in tickers:
            self.stdout.write(f'Processing {t}...')
            try:
                result = run_pipeline_for_ticker(t, skip_fundamentals=options['skip_fundamentals'])
                if result['prices_updated']:
                    self.stdout.write(f'  Saved price history')
                else:
                    self.stdout.write(f'  Prices already up to date, skipping')
                if not options['skip_fundamentals']:
                    if result['fundamentals_updated']:
                        self.stdout.write(f'  Saved fundamentals')
                    else:
                        self.stdout.write(f'  Fundamentals already up to date, skipping')
                self.stdout.write(self.style.SUCCESS(f'  {t} done'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  {t} failed: {e}'))
