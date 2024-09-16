from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def knasta(driver):
    driver.get("https://knasta.cl/results?q=perfumes")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'body-principal')))

    data = []
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll hasta el final de la página para cargar todos los productos
        etiquetas = driver.find_elements(By.XPATH,'//a[@data-tag-key="results_listing_products"]')

        # Encuentra la etiqueta que contiene la información que deseas
        for etiqueta in etiquetas:
            # Extrae el nombre del perfume
            marca = etiqueta.find_element(By.XPATH, './/div[contains(@class, "text-xs")]//span[contains(@class, "font-bold")]').text
            nombre_perfume = etiqueta.find_element(By.XPATH, './/div[contains(@class, "text-xs text-black_1 betterhover:group-hover:font-semibold line-clamp-2 h-8 mt-2")]').text
            indice_perfume = nombre_perfume.lower().find("perfume")
            nombre_perfume = nombre_perfume[indice_perfume + len("perfume"):].strip()
            # Verificar si el perfume es para hombres
            # if "mujer" in nombre_perfume.lower():  # Convertir a minúsculas para la comparación
            #     continue
            # Extrae el precio
            precio = etiqueta.find_element(By.XPATH, './/div[contains(@class, "font-bold")]').text

            # Extrae el enlace (link)
            enlace = etiqueta.get_attribute('href')

            data.append({'Marca': marca, 'Nombre del perfume': nombre_perfume, 'Precio': float(''.join(filter(str.isdigit, precio))), 'Enlace': enlace})
        
        try:
            # Busca el botón de "Siguiente" y haz clic en él
            next_button = driver.find_element(By.XPATH, '//button[@data-tag-value="siguiente"]')
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print(e, 'Bot terminó de recorrer la página')
            # Si no se encuentra el botón de "Siguiente", sal del bucle
            break


     # Crea un DataFrame con los datos recolectados
    df = pd.DataFrame(data)
   
    driver.quit()
    return df

def lodoro(driver):
    driver.get("https://www.lodoro.cl/collections/perfumes-de-hombre")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, './/div[contains(@class, "container container--flush")]')))
    
    data = []

    while True:
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll hasta el final de la página para cargar todos los productos
        etiquetas = driver.find_elements(By.XPATH,'//div[@class="product-item__info"]')
        
        # Encuentra la etiqueta que contiene la información que deseas
        for etiqueta in etiquetas:
            # Extrae el nombre del perfume
            marca = etiqueta.find_element(By.XPATH, './/a[contains(@class, "product-item__vendor link")]').text
            nombre_perfume = etiqueta.find_element(By.XPATH, './/a[contains(@class, "product-item__title text--strong link")]').text 
            # Extrae el precio
            try:
                precio = etiqueta.find_element(By.XPATH, './/span[contains(@class, "price--highlight")]').text
            except:
                precio = etiqueta.find_element(By.XPATH, './/span[contains(@class, "price")]').text
                raise

                
            # Extrae el enlace (link)
            enlace_element = etiqueta.find_element(By.XPATH, './/a[contains(@class, "product-item__title")]')
            enlace = enlace_element.get_attribute('href')
            
            data.append({'Marca': marca, 'Nombre del perfume': nombre_perfume, 'Precio': float(''.join(filter(str.isdigit, precio))), 'Enlace': enlace})
            
        try:
            # Buscar el botón de "Siguiente" en la paginación y hacer clic en él
            next_button = driver.find_element(By.XPATH, '//a[@class="pagination__next link"]')
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print('Bot terminó de recorrer la página')
            # Si no se encuentra el botón de "Siguiente", salir del bucle
            break


    # Crea un DataFrame con los datos recolectados
    df = pd.DataFrame(data)

    driver.quit()
    return df

