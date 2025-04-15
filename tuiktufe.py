from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# WebDriver'ı başlatma
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# TÜİK haber bülteni sayfasına gitme
url = "https://data.tuik.gov.tr/Search/Search?text=t%C3%BCfe"
driver.get(url)

# Sayfanın yüklenmesi için biraz bekle
time.sleep(5)

try:
    # "Tüketici Fiyat Endeksi" başlıklarını içeren tüm <a> etiketlerini al
    headlines = driver.find_elements(By.XPATH, "//a[contains(text(),'Tüketici Fiyat Endeksi')]")
    
    if headlines:
        # Başlıklar arasındaki en üsttekini almak
        first_headline = headlines[0]
        
        # En üstteki başlık metnini al
        headline_text = first_headline.text
        print("Başlık:", headline_text)
        
        # Başlığın bulunduğu div'i bul
        parent_div = first_headline.find_element(By.XPATH, "./ancestor::div[contains(@class, 'news-content')]")
        
        # İçeriği içeren <p> etiketini bul
        content = parent_div.find_element(By.XPATH, ".//p[contains(@class, 'text-secondary')]")
        
        # İçeriği yazdır
        print("Bülten İçeriği:")
        print(content.text)
    else:
        print("Tüketici Fiyat Endeksi başlığı bulunamadı.")
    
except Exception as e:
    print(f"Hata oluştu: {e}")

finally:
    driver.quit()
