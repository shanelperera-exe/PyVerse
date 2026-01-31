import aiohttp
import asyncio
from config import REQUEST_TIMEOUT, USER_AGENT, MAX_RETRIES, BACKOFF_BASE

class Fetcher:
    def __init__(self, session, semaphore):
        self.session = session
        self.semaphore = semaphore

    async def fetch(self, url):
        for attempt in range(1, MAX_RETRIES + 1):
            async with self.semaphore:
                try:
                    async with self.session.get(
                        url,
                        timeout=REQUEST_TIMEOUT,
                        headers={"User-Agent": USER_AGENT}
                    ) as response:
                        html = await response.text()
                        return {
                            "url": url,
                            "status": response.status,
                            "html": html,
                            "attempts": attempt,
                        }

                except asyncio.TimeoutError:
                    error = "timeout"
                except aiohttp.ClientError as e:
                    error = str(e)

            if attempt < MAX_RETRIES:
                backoff = BACKOFF_BASE * (2 ** (attempt - 1))
                await asyncio.sleep(backoff)

        return {
            "url": url,
            "status": "failed",
            "html": None,
            "attempts": MAX_RETRIES,
            "error": error,
        }
