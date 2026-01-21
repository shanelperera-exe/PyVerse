from threading import Thread
from multiprocessing import Process
import requests

class ImageDownloader(Process):
    def __init__(self, thread_id, name, urls, results):
        super(ImageDownloader, self).__init__()
        self.id = thread_id
        self.name = name
        self.urls = urls
        self.success_count = 0
        self.results = results

    def run(self):
        for i, url in enumerate(self.urls):
            if self.download_img(url, f"{self.id}-{i}"):
                self.success_count += 1

        self.results.put(self.success_count)

    def download_img(self, url, img_no):
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        filename = f"images/{img_no}.jpg"
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
                print(f"Image downloaded successfully as {filename.split("/")[1]}")
                return True
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return False