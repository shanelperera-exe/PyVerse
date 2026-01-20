import requests
from random import randint
import time

def get_image_urls(count):
    if count <= 0:
        print("Invalid count")
        return

    for _ in range(0, count):
        id = randint(0, 500)
        url = f"https://picsum.photos/id/{id}/1280/720"
        yield url

def download_imgs(image_urls):
    for img_no, url in enumerate(image_urls):
        download_img(img_no, url)

def download_img(img_no, url):
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    filename = f"images/{img_no}.jpg"
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
            print(f"Image downloaded successfully as {filename.split("/")[1]}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def main():
    start = time.time_ns()

    urls = get_image_urls(10)
    download_imgs(urls)

    diff = time.time_ns() - start
    print(f"Program Duration: {diff / 1000000}")


if __name__ == "__main__":
    main()