from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from io import BytesIO

# WebDriver başlatma
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Sayfayı açma
url = "https://data.tuik.gov.tr/Search/Search?text=T%C3%BCketici%20Fiyat%20Endeksi"
driver.get(url)

# İlk tıklama işlemi 
try:
    # XPath ile öğeyi bulma ve görünür olana kadar bekleme
    xpath1 = '/html/body/div[2]/div[2]/div[2]/div/nav/div/a[2]'
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath1))
    )
    
    # İlk öğeye tıklama
    element1 = driver.find_element(By.XPATH, xpath1)
    element1.click()
    print("İlk tıklama işlemi başarılı!")
    
    # Sayfanın tamamen yüklenmesi için bekleme
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/table/tbody/tr[3]/td[3]/a'))
    )
except Exception as e:
    print(f"İlk tıklama hatası: {e}")

# İkinci XPath ile Excel dosyasının indirme linkini almak
try:
    # İkinci XPath ile <a> etiketini bulma ve görünür olana kadar bekleme
    xpath2 = '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/table/tbody/tr[3]/td[3]/a'
    
    # Sayfanın tamamen yüklendiğinden emin olduktan sonra öğeyi bulma
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath2))
    )
    
    # İkinci öğeyi al
    element2 = driver.find_element(By.XPATH, xpath2)
    download_link = element2.get_attribute('href')  # href özelliğini al
    
    print("İndirme linki bulundu:", download_link)
    
    # Excel dosyasını indirip içeriği okuma
    response = requests.get(download_link)
    if response.status_code == 200:
        # Dosyayı belleğe al
        excel_file = BytesIO(response.content)
        
        # Pandas ile veriyi doğrudan okuma
        raw_df = pd.read_excel(excel_file, header=None, engine='xlrd')

        # 2005 satırını bul ve veriyi o satırdan al
        start_row = raw_df[raw_df.iloc[:, 0] == 2005].index[0]

        # 2025 satırını bul ve bitişi o satırda kabul et
        end_row = raw_df[raw_df.iloc[:, 0] == 2025].index[0]

        # Veriyi başlıklar olmadan çek, 'start_row' ile 'end_row' arasındaki kısmı al
        table_df = pd.read_excel(excel_file, header=None, engine='xlrd', skiprows=start_row, nrows=end_row - start_row + 1, index_col=0)

        # İlk 25 satırı göster
        print(table_df.head(25))  # İlk 25 satırı yazdır
    else:
        print("Dosya indirilemedi.")
    
except Exception as e:
    print(f"İkinci XPath ile işlem hatası: {e}")

# Tarayıcıyı kapatma
driver.quit()
