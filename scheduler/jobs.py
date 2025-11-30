from apscheduler.schedulers.asyncio import AsyncIOScheduler
from crawler.crawler import crawl_all
from db.mongo import get_db
from scheduler.report import generate_report
from utilities.logger import setup_logger


logger = setup_logger(__name__)



async def crawl_and_detect_changes():
    """
    Crawl the site, detect new or updated books, and store changes in MongoDB.
    """
    try:
        db = get_db()
        logger.info("Starting scheduled daily crawl...")
        await crawl_all()
        logger.info("Scheduled Crawl finished successfully")

        # Optional: generate daily report
        await generate_report()
        logger.info("Daily change report generated")
    except Exception as e:
        logger.exception(f"Error during daily crawl: {e}")



def init_scheduler():
    scheduler = AsyncIOScheduler()
    
    # Schedule the crawl daily at 2:00 AM
    scheduler.add_job(crawl_and_detect_changes, "cron",hour="17", minute="24")
    
    scheduler.start()
    logger.info("Scheduler started. Waiting for jobs...")

   

