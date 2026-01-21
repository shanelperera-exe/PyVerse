from random import randint
import time
import my_thread
import os
from queue import Queue

def get_image_urls(count):
    if count <= 0:
        print("Invalid count")
        return

    for _ in range(0, count):
        id = randint(0, 500)
        url = f"https://picsum.photos/id/{id}/1280/720"
        yield url

def main():
    start = time.time_ns()

    urls = list(get_image_urls(100))

    urls_list = []
    num_of_threads = 10

    for i in range(0, len(urls), num_of_threads):
        l = urls[i : i + num_of_threads]
        urls_list.append(l)

    threads = []
    results = Queue()

    for i in range(0, num_of_threads):
        thread = my_thread.ImageDownloader(i, f"Thread-{i}", urls_list[i], results)
        os.makedirs("images", exist_ok=True)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    success_count = 0

    while not results.empty():
        success_count += results.get()

    print(f"{success_count} images downloaded successfully.")

    diff = time.time_ns() - start
    print(f"Program Duration: {diff / 1000000}")


if __name__ == "__main__":
    main()