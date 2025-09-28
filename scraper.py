import time
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from google.oauth2.service_account import Credentials
from datetime import datetime


class WebScraperToSheets:
    def __init__(self, credentials_file, spreadsheet_name, worksheet_name="Datos"):
        """
        Inicializar el scraper
        
        Args:
            credentials_file (str): Ruta al archivo JSON de credenciales de Google
            spreadsheet_name (str): Nombre de la hoja de Google Sheets
            worksheet_name (str): Nombre de la pestaña dentro del spreadsheet
        """
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.worksheet_name = worksheet_name
        self.driver = None
        self.gc = None
        self.worksheet = None
        
    def setup_driver(self, headless=True):
        """Configurar el driver de Chrome"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
    
    def setup_google_sheets(self):
        """Configurar conexión con Google Sheets"""
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials = Credentials.from_service_account_file(
            self.credentials_file, scopes=scope
        )
        
        self.gc = gspread.authorize(credentials)
        spreadsheet = self.gc.open(self.spreadsheet_name)
        
        # Crear o abrir worksheet
        try:
            self.worksheet = spreadsheet.worksheet(self.worksheet_name)
        except gspread.WorksheetNotFound:
            self.worksheet = spreadsheet.add_worksheet(
                title=self.worksheet_name, rows="1000", cols="20"
            )
            
        return self.worksheet
    
    def scrape_example_site(self, url):
        """
        Ejemplo de scraping - modifica esta función según tu sitio web objetivo
        
        Args:
            url (str): URL del sitio web a scrapear
            
        Returns:
            list: Lista de diccionarios con los datos scrapeados
        """
        self.driver.get(url)
        
        # Esperar a que la página cargue
        wait = WebDriverWait(self.driver, 10)
        
        data = []
        
        try:
            # Ejemplo: Scrapear títulos y enlaces de noticias
            # Modifica estos selectores según tu sitio web
            titles = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "h2 a, h3 a, .title a")
            ))
            
            for i, title in enumerate(titles[:10]):  # Limitar a 10 elementos
                try:
                    title_text = title.text.strip()
                    link = title.get_attribute('href')
                    
                    # También puedes extraer más información
                    # Por ejemplo, descripción, fecha, etc.
                    
                    data.append({
                        'titulo': title_text,
                        'enlace': link,
                        'fecha_scraping': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'posicion': i + 1
                    })
                    
                except Exception as e:
                    print(f"Error extrayendo elemento {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error durante el scraping: {e}")
            
        return data
    
    def scrape_custom_data(self, url, selectors_config):
        """
        Función genérica para scraping personalizado
        
        Args:
            url (str): URL del sitio web
            selectors_config (dict): Configuración de selectores
                Ejemplo: {
                    'titulo': 'h2.title',
                    'precio': '.price',
                    'descripcion': '.description'
                }
        """
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        
        data = []
        
        try:
            # Encontrar todos los contenedores principales
            containers = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, selectors_config.get('container', 'div'))
            ))
            
            for i, container in enumerate(containers):
                item_data = {
                    'fecha_scraping': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'posicion': i + 1
                }
                
                for field_name, selector in selectors_config.items():
                    if field_name in ['container']:
                        continue
                        
                    try:
                        element = container.find_element(By.CSS_SELECTOR, selector)
                        item_data[field_name] = element.text.strip()
                    except:
                        item_data[field_name] = ''
                
                data.append(item_data)
                
        except Exception as e:
            print(f"Error durante el scraping personalizado: {e}")
            
        return data
    
    def send_to_sheets(self, data):
        """
        Enviar datos a Google Sheets
        
        Args:
            data (list): Lista de diccionarios con los datos
        """
        if not data:
            print("No hay datos para enviar")
            return
        
        # Obtener headers de los datos
        headers = list(data[0].keys())
        
        # Verificar si ya existen headers en la hoja
        try:
            existing_headers = self.worksheet.row_values(1)
            if not existing_headers:
                # Agregar headers si la hoja está vacía
                self.worksheet.append_row(headers)
        except:
            # Si hay error, agregar headers
            self.worksheet.append_row(headers)
        
        # Preparar datos para insertar
        rows = []
        for item in data:
            row = [item.get(header, '') for header in headers]
            rows.append(row)
        
        # Insertar datos
        if rows:
            self.worksheet.append_rows(rows)
            print(f"Se enviaron {len(rows)} filas a Google Sheets")
    
    def run_scraping(self, url, selectors_config=None):
        """
        Ejecutar todo el proceso de scraping
        
        Args:
            url (str): URL a scrapear
            selectors_config (dict, optional): Configuración de selectores personalizados
        """
        try:
            # Configurar driver y Google Sheets
            self.setup_driver()
            self.setup_google_sheets()
            
            # Realizar scraping
            if selectors_config:
                data = self.scrape_custom_data(url, selectors_config)
            else:
                data = self.scrape_example_site(url)
            
            # Enviar a Google Sheets
            self.send_to_sheets(data)
            
            print("Proceso completado exitosamente")
            
        except Exception as e:
            print(f"Error en el proceso: {e}")
        finally:
            if self.driver:
                self.driver.quit()

# Ejemplo de uso
if __name__ == "__main__":
    # Configuración
    CREDENTIALS_FILE = "path/to/your/google-credentials.json"
    SPREADSHEET_NAME = "Mi Hoja de Scraping"
    
    # Crear instancia del scraper
    scraper = WebScraperToSheets(CREDENTIALS_FILE, SPREADSHEET_NAME)
    
    # Ejemplo 1: Scraping básico
    url = "https://example.com"
    scraper.run_scraping(url)
    
    # Ejemplo 2: Scraping personalizado
    selectors_config = {
        'container': '.product-item',
        'titulo': 'h3.product-title',
        'precio': '.price',
        'descripcion': '.product-desc'
    }
    
    # scraper.run_scraping("https://ejemplo-tienda.com", selectors_config)

# Función adicional para scraping programado
def scheduled_scraping():
    """Función para ejecutar scraping de forma programada"""
    import schedule
    
    def job():
        scraper = WebScraperToSheets(
            "path/to/credentials.json", 
            "Mi Hoja de Scraping"
        )
        scraper.run_scraping("https://example.com")
    
    # Programar para ejecutar cada hora
    schedule.every().hour.do(job)
    
    # Mantener el programa ejecutándose
    while True:
        schedule.run_pending()
        time.sleep(60)