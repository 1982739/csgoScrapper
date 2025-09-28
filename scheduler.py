import time
from main import run_scraping

def scheduled_scraping():
    import schedule
    def job():
        run_scraping(
            "path/to/credentials.json",
            "Mi Hoja de Scraping",
            "https://example.com"
        )
    schedule.every().hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    scheduled_scraping()
