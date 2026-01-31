import asyncio
from urllib.parse import urlparse
from config import MAX_CONCURRENT_REQUESTS

# Dictionary to hold semaphores per domain
domain_limits = {}

def get_domain_semaphore(url):
    """
    Return a semaphore for the domain of the URL.
    Ensures per-domain rate limiting.
    """
    domain = urlparse(url).netloc
    if domain not in domain_limits:
        domain_limits[domain] = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    return domain_limits[domain]


async def worker(name, queue, fetcher, parser, results, progress, visited, max_depth):
    while True:
        url, depth = await queue.get()
        try:
            # Placeholder for optional features in Phase 3 (robots, custom link extraction)
            fetched = await fetcher.fetch(url)
            parsed = parser(fetched.get("html"))

            results.append({
                "url": url,
                "status": fetched["status"],
                "data": parsed,
                "error": fetched.get("error"),
                "depth": depth,
            })

            progress["done"] += 1
            print(f"[{name}] processed {url} ({progress['done']}/{progress['total']}) Depth={depth}")

            # Queue discovered links
            # NOTE: Link discovery is handled in run_pipeline via the injected extractor.

        finally:
            queue.task_done()


async def run_pipeline(urls, fetcher, parser, worker_count=3, max_depth=0, link_extractor=None, robots=None):
    """
    Run the async crawling pipeline.
    """
    queue = asyncio.Queue()
    results = []
    visited = set()
    progress = {"done": 0, "total": len(urls)}

    if link_extractor is None:
        link_extractor = lambda _html, _base_url: []

    # Seed URLs, starting at depth 0
    for url in urls:
        await queue.put((url, 0))
        visited.add(url)

    async def phase3_worker(name):
        while True:
            url, depth = await queue.get()
            try:
                if robots is not None:
                    allowed = await robots.allowed(url)
                    if not allowed:
                        results.append({
                            "url": url,
                            "status": "blocked_by_robots",
                            "data": None,
                            "error": None,
                            "depth": depth,
                        })
                        progress["done"] += 1
                        print(f"[{name}] blocked by robots {url} ({progress['done']}/{progress['total']}) Depth={depth}")
                        continue

                fetched = await fetcher.fetch(url)
                parsed = parser(fetched.get("html"))

                results.append({
                    "url": url,
                    "status": fetched.get("status"),
                    "data": parsed,
                    "error": fetched.get("error"),
                    "depth": depth,
                })

                progress["done"] += 1
                print(f"[{name}] processed {url} ({progress['done']}/{progress['total']}) Depth={depth}")

                if fetched.get("html") and depth < max_depth:
                    for link in link_extractor(fetched["html"], url):
                        if link in visited:
                            continue
                        visited.add(link)
                        await queue.put((link, depth + 1))
                        progress["total"] += 1

            finally:
                queue.task_done()

    # Start workers
    workers = [asyncio.create_task(phase3_worker(f"Worker-{i}")) for i in range(worker_count)]

    try:
        await queue.join()  # Wait until all tasks are done
    except asyncio.CancelledError:
        print("Pipeline cancelled! Shutting down workers...")
    finally:
        # Cancel all workers to clean up
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    return results
