import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import urllib.request
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-notifications")

# initializing webdriver and open the Chrome window
driver = webdriver.Chrome(options=chrome_options)

# use '.get' to open the site via link
driver.get("https://ru.depositphotos.com/")

# looking for the element by name="query" in html
textarea = driver.find_element(By.NAME, "query")

# Enter the text into previously found textarea. Use "\n" to send keyboard-keypress "ENTER".
search_query = input('Insert search query: ')
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

# create directory in current folder if not exist
if not os.path.isdir('Downloads'):
    print("Creating directory 'Downloads'")
    os.mkdir('Downloads')


# saving images on harddisk
async def download_img(url):
    def func_for_executor():
        print(f"Start downloading file {urls_img.index(url)}")
        urllib.request.urlretrieve(url, f"./Downloads/{search_query}_{urls_img.index(url)}.jpg")
        print(f"Finished downloading file {urls_img.index(url)}")

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=None) as executor:
        print(f'ThreadPoolExecutor started')
        # print(f'{executor=}')
        await loop.run_in_executor(executor, func_for_executor)
        print(f'ThreadPoolExecutor finished')


async def main(urls_img_):
    tasks = []
    for url in urls_img_:
        tasks.append(asyncio.create_task(download_img(url)))

    for task in tasks:
        await task


start = time.time()
asyncio.run(main(urls_img))
end = time.time() - start
print(f"Time {end} sec")
# close browser window
driver.quit()
