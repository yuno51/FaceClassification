import os
import time
from selenium import webdriver
import chromedriver_binary
from PIL import Image
import io
import requests
import hashlib
import sys


def scraping_image(search_word, search_url, download_num = 200, sleep_interval = 0.5):
    #画像のurlの取得
    wd = webdriver.Chrome()
    wd.get(search_url.format(q=search_word))
    thumbnail_results = wd.find_elements_by_css_selector("img.rg_i")

    image_urls = set()
    for i, img in enumerate(thumbnail_results[:download_num]):
        print(i, img)
        try:
            img.click()
            time.sleep(sleep_interval)
        except Exception as e:
            continue
        candidates = wd.find_elements_by_class_name('n3VNCb')
        for candidate in candidates:
            try:
                url = candidate.get_attribute('src')
                if url and 'https' in url:
                    image_urls.add(url)
            except:
                continue
    time.sleep(3)
    wd.quit()

    #画像のダウンロード
    now_dir = os.getcwd()
    base_dir = os.path.join(now_dir, "images/original")
    image_dir = os.path.join(base_dir, search_word)

    if not os.path.exists(base_dir): os.mkdir(base_dir)
    if not os.path.exists(image_dir): os.mkdir(image_dir)

    for url in image_urls:
        try:
            image_content = requests.get(url).content
        except:
            print(f"ERROR - Could not download")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(image_dir,f"{hashlib.sha1(image_content).hexdigest()[:10]}.png")
            with open(file_path, 'wb') as f:
                image.save(f, "PNG")
            print(f"SUCCESS - saved {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {e}")


def main():
    try:
        search_word = sys.argv[1]
    except:
        raise Exception("Please set the search term in the argument.")
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    scraping_image(search_word, search_url)

if __name__ == "__main__":
    main()