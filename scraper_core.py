from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def scrape_example_site(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    data = []
    try:
        titles = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "h2 a, h3 a, .title a")
        ))
        for i, title in enumerate(titles[:10]):
            try:
                title_text = title.text.strip()
                link = title.get_attribute('href')
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

def scrape_custom_data(driver, url, selectors_config):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    data = []
    try:
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
