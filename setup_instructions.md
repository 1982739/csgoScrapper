# Configuración del Web Scraper con Selenium y Google Sheets

## 1. Instalación de dependencias

Instala las librerías necesarias usando pip:

```bash
pip install selenium gspread google-auth webdriver-manager schedule
```

## 2. Configuración de Google Sheets API

### Paso 1: Crear proyecto en Google Cloud
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita Google Sheets API y Google Drive API

### Paso 2: Crear credenciales de servicio
1. Ve a "Credenciales" → "Crear credenciales" → "Cuenta de servicio"
2. Completa el formulario y crea la cuenta
3. En la cuenta de servicio creada, ve a "Claves" → "Agregar clave" → "JSON"
4. Descarga el archivo JSON (serán tus credenciales)

### Paso 3: Compartir tu Google Sheets
1. Crea una nueva hoja de Google Sheets
2. Comparte la hoja con el email de la cuenta de servicio (encontrarás el email en el archivo JSON)
3. Dale permisos de editor

## 3. Estructura del archivo de credenciales

Tu archivo JSON de credenciales debe verse así:

```json
{
  "type": "service_account",
  "project_id": "tu-proyecto-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "tu-servicio@tu-proyecto.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

## 4. Ejemplo de uso básico

```python
from web_scraper import WebScraperToSheets

# Configurar scraper
scraper = WebScraperToSheets(
    credentials_file="ruta/a/tu/credenciales.json",
    spreadsheet_name="Nombre de tu hoja de Google Sheets"
)

# Ejecutar scraping básico
scraper.run_scraping("https://sitio-web.com")
```

## 5. Ejemplo de uso avanzado con selectores personalizados

```python
# Configuración de selectores para un sitio específico
selectors_config = {
    'container': '.product-item',  # Contenedor principal de cada elemento
    'titulo': 'h3.product-title',  # Selector para el título
    'precio': '.price',            # Selector para el precio  
    'descripcion': '.description', # Selector para la descripción
    'imagen': 'img'                # Selector para imagen
}

# Ejecutar scraping personalizado
scraper.run_scraping("https://tienda-online.com", selectors_config)
```

## 6. Programar scraping automático

```python
import schedule
import time

def job():
    scraper = WebScraperToSheets("credenciales.json", "Mi Hoja")
    scraper.run_scraping("https://example.com")

# Programar ejecuciones
schedule.every().hour.do(job)        # Cada hora
schedule.every().day.at("09:00").do(job)  # Diario a las 9 AM
schedule.every().monday.do(job)      # Cada lunes

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 7. Notas importantes

- **Respecta el robots.txt**: Verifica que el sitio web permita scraping
- **Usa delays**: Agrega pausas entre requests para no sobrecargar el servidor
- **Maneja errores**: El código incluye manejo de errores básico
- **Personaliza selectores**: Modifica los selectores CSS según el sitio web objetivo
- **Privacidad**: Mantén tus credenciales seguras y no las subas a repositorios públicos

## 8. Consejos para encontrar selectores CSS

1. **Inspeccionar elemento**: Clic derecho → "Inspeccionar elemento"
2. **Selectores comunes**:
   - Por clase: `.nombre-clase`
   - Por ID: `#id-elemento`
   - Por tag: `h1`, `div`, `a`
   - Combinados: `div.clase h2 a`
3. **Herramientas del navegador**: Usa la consola para probar selectores con `document.querySelector()`

## 9. Solución de problemas comunes

- **Error de credenciales**: Verifica que el archivo JSON esté en la ruta correcta
- **Hoja no encontrada**: Asegúrate de compartir la hoja con el email de servicio
- **Elementos no encontrados**: Revisa los selectores CSS y espera a que la página cargue
- **Chrome no encontrado**: webdriver-manager descargará automáticamente ChromeDriver