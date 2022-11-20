import time
import urllib.request
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# initializing webdriver and open the Chrome window
driver = webdriver.Chrome()

# use '.get' to open the site via link
driver.get("https://ru.depositphotos.com/")

# looking for the element by name="query" in html
textarea = driver.find_element(By.NAME, "query")

# Enter the text into previously found textarea. Use "\n" to send keyboard-keypress "ENTER".
search_query = "flower"
textarea.send_keys(f"{search_query}\n")
time.sleep(1)

# getting html elements wth image
web_elements_with_image = driver.find_elements(By.CSS_SELECTOR, "img")
print(web_elements_with_image)
# print(len(web_elements_with_image))

# list for collecting images' urls
urls_img = []

# error when use .get_attribute with list (web_elements_with_image.get_attribute), so will use
# .get_attribute with single element
for web_element in web_elements_with_image[:10]:
    url_img = web_element.get_attribute('src')
    urls_img.append(url_img)
print(urls_img)
# root > div > main > div._content.content-container.content_search > section > section > article > section > div > div._files-list > div > div.flex-files.flex-files_xwide.flex-files_like-grid._slider > section:nth-child(14) > a > picture > img

# image.click()

# create directory in current folder if not exist
if not os.path.isdir('Downloads'):
    print("Creating directory 'Downloads'")
    os.mkdir('Downloads')

start = time.time()
# saving images on harddisk
for i in range(len(urls_img)):
    urllib.request.urlretrieve(urls_img[i], f"./Downloads/{search_query}_{i}.jpg")
    print(f"Downloading file {i}")
    time.sleep(1)
end = time.time() - start
print(f"Time {end} sec")
# close browser window
driver.quit()
