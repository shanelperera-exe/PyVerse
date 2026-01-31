from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import aiohttp


def _robots_txt_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))


@dataclass
class RobotsCache:
    session: aiohttp.ClientSession
    semaphore: asyncio.Semaphore
    user_agent: str
    timeout: float | int

    _cache: Dict[str, Optional[RobotFileParser]] = None
    _locks: Dict[str, asyncio.Lock] = None

    def __post_init__(self) -> None:
        self._cache = {}
        self._locks = {}

    async def allowed(self, url: str) -> bool:
        parts = urlsplit(url)
        key = parts.netloc
        if not key:
            return True

        rp = await self._get_or_fetch(key, url)
        if rp is None:
            return True
        return rp.can_fetch(self.user_agent, url)

    async def _get_or_fetch(self, key: str, sample_url: str) -> Optional[RobotFileParser]:
        if key in self._cache:
            return self._cache[key]

        lock = self._locks.get(key)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[key] = lock

        async with lock:
            if key in self._cache:
                return self._cache[key]

            robots_url = _robots_txt_url(sample_url)
            try:
                async with self.semaphore:
                    async with self.session.get(
                        robots_url,
                        headers={"User-Agent": self.user_agent},
                        timeout=self.timeout,
                    ) as resp:
                        if resp.status >= 400:
                            self._cache[key] = None
                            return None
                        text = await resp.text()
            except Exception:
                # Fail-open: if robots can't be retrieved, don't block crawling.
                self._cache[key] = None
                return None

            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.parse(text.splitlines())
            self._cache[key] = rp
            return rp
