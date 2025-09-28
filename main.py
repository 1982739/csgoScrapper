from driver_setup import setup_driver
from sheets_manager import SheetsManager
from scraper_core import scrape_example_site, scrape_custom_data


def run_scraping(credentials_file, spreadsheet_name, url, selectors_config=None):
    driver = None
    try:
        driver = setup_driver()
        sheets = SheetsManager(credentials_file, spreadsheet_name)
        sheets = sheets.setup_google_sheets()
        if selectors_config:
            data = scrape_custom_data(driver, url, selectors_config)
        else:
            data = scrape_example_site(driver, url)
        sheets.send_to_sheets(data)
        print("Proceso completado exitosamente")
    except Exception as e:
        print(f"Error en el proceso: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    CREDENTIALS_FILE = "path/to/your/google-credentials.json"
    SPREADSHEET_NAME = "Mi Hoja de Scraping"
    url = "https://example.com"
    run_scraping(CREDENTIALS_FILE, SPREADSHEET_NAME, url)
    # Ejemplo de scraping personalizado:
    # selectors_config = {
    #     'container': '.product-item',
    #     'titulo': 'h3.product-title',
    #     'precio': '.price',
    #     'descripcion': '.product-desc'
    # }
    # run_scraping(CREDENTIALS_FILE, SPREADSHEET_NAME, "https://ejemplo-tienda.com", selectors_config)
