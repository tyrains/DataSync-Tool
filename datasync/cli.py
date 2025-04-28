"""
Command-line interface for DataSync-Tool.
"""

import click
from loguru import logger
from .sync import DataSync

@click.group()
def cli():
    """DataSync-Tool - A tool for synchronizing data between cloud services and local storage."""
    pass

@cli.command()
@click.option('--config', '-c', required=True, help='Path to configuration file')
def sync(config):
    """Run synchronization based on configuration."""
    try:
        logger.info(f"Loading configuration from {config}")
        sync_tool = DataSync(config)
        sync_tool.sync()
    except Exception as e:
        logger.error(f"Error during synchronization: {e}")
        raise click.ClickException(str(e))

@cli.command()
@click.option('--config', '-c', required=True, help='Path to configuration file')
@click.option('--schedule', '-s', help='Cron-style schedule (e.g., "0 0 * * *" for daily at midnight)')
def schedule(config, schedule):
    """Schedule regular synchronization based on configuration."""
    try:
        import schedule
        import time
        
        logger.info(f"Scheduling sync with configuration from {config}")
        sync_tool = DataSync(config)
        
        def run_sync():
            try:
                sync_tool.sync()
            except Exception as e:
                logger.error(f"Error in scheduled sync: {e}")
        
        # Schedule the sync
        schedule.every().day.at(schedule).do(run_sync)
        
        logger.info(f"Scheduled sync to run {schedule}")
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except Exception as e:
        logger.error(f"Error setting up schedule: {e}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli() 