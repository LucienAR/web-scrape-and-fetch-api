import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.service import Service


# กำหนด path ของ geckodriver (หากต้องใช้)
# service = Service('/path/to/geckodriver')
# driver = webdriver.Firefox(service=service, options=options)
search = input("Enter the search term: ")

options = Options()
driver = webdriver.Firefox(options=options)

driver.get("https://www.ebay.com/")

# XPATH
# search_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, '//input[@class="gh-tb ui-autocomplete-input"]'))
# )

# Search
# CSS_SELECTOR
# รอจนกว่าช่องค้นหาจะพร้อม
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,'input.gh-tb.ui-autocomplete-input'))
)
search_box.send_keys(search)
search_box.send_keys(Keys.RETURN)

# รอจนกว่าผลลัพธ์จะโหลด
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-item__info'))
)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# สร้างListของข้อมูลที่ต้องการ ในที่นี้คือ ชื่อสินค้า ราคาขั้นต่ำและจำนวนที่ขายไป
product_names_list = []
prices_list = []
solds_list = []

items = soup.find_all("div", {"class" : "s-item__info"})

for item in items:
    name = item.find("div", {"class" :"s-item__title"})
    price = item.find("span", {"class" : "s-item__price"})
    sold = item.find("span",{"class" : "s-item__dynamic s-item__quantitySold"})
    
    if name:
        clean_product = name.get_text().strip()
        product_names_list.append(clean_product)
    else:
        product_names_list.append("")
        
    if price:
        get_price = price.get_text().strip()
        cleaned_price = re.sub(r'THB|to.*', '', get_price) # เอา THB ออก รวมถึง to และข้อความหลังto ราคาที่ได้จะเป็น Min
        cleaned_price = re.sub(r'[^\d.]', '', cleaned_price) # เหลือเฉพาะตัวเลขและจุดทศนิยม
        
        cleaned_price = float(cleaned_price) # แปลงเป็น float เพื่อความชัว
        
        # print(type(cleaned_price)) 
        
        prices_list.append(cleaned_price)
    else:
        prices_list.append("")
        
    if sold:
        get_sold = sold.get_text().strip()
        cleaned_sold = re.sub(r'[^\d.]', '', get_sold)
        
        try:
            cleaned_sold = float(cleaned_sold)
        except ValueError:
            cleaned_sold = 0.0
        
        cleaned_sold = int(cleaned_sold)
        
        # print(type(cleaned_sold))
        
        solds_list.append(cleaned_sold)
        
    else:
        solds_list.append("")
        

data = {
    'Product Name' : product_names_list,
    'Price' : prices_list,
    'Sold' : solds_list 
}

driver.quit()

# สร้าง data frame
df = pd.DataFrame(data)

# save เป็น csv 
df.to_csv('ebay_products_prices_solds.csv', index=False)

print(df)
