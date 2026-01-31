import argparse
import asyncio
from pathlib import Path

import aiohttp

from config import MAX_CONCURRENT_REQUESTS, REQUEST_TIMEOUT, USER_AGENT
from crawler.fetcher import Fetcher
from crawler.output import save_csv, save_json
from crawler.parser import extract_links, parse
from crawler.pipeline import run_pipeline
from crawler.robots import RobotsCache


DEFAULT_URLS = [
    "https://example.com",
]


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Async web crawler")
    p.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="Seed URL (repeatable). If omitted, uses built-in defaults.",
    )
    p.add_argument(
        "--urls-file",
        type=Path,
        help="Path to a text file with one seed URL per line.",
    )
    p.add_argument(
        "--depth",
        type=int,
        default=0,
        help="Crawl depth from seeds (0 = only seed URLs). Default: 0.",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=3,
        help="Number of worker tasks. Default: 3.",
    )
    p.add_argument(
        "--max-concurrent",
        type=int,
        default=MAX_CONCURRENT_REQUESTS,
        help=f"Max concurrent HTTP requests. Default: {MAX_CONCURRENT_REQUESTS}.",
    )
    p.add_argument(
        "--respect-robots",
        action="store_true",
        help="Respect robots.txt (fail-open if robots.txt can't be fetched).",
    )
    p.add_argument(
        "--output",
        type=Path,
        help="Write results to a file (.json or .csv). If omitted, only prints results.",
    )
    p.add_argument(
        "--format",
        choices=["json", "csv"],
        help="Output format when using --output. If omitted, inferred from file extension.",
    )
    return p


def _load_urls(args: argparse.Namespace) -> list[str]:
    urls: list[str] = []

    if args.urls:
        urls.extend(args.urls)

    if args.urls_file:
        text = args.urls_file.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)

    if not urls:
        urls = list(DEFAULT_URLS)

    return urls


def _infer_format(output: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    if output.suffix.lower() == ".csv":
        return "csv"
    return "json"


async def main_async(args: argparse.Namespace) -> int:
    urls = _load_urls(args)
    semaphore = asyncio.Semaphore(args.max_concurrent)

    async with aiohttp.ClientSession() as session:
        fetcher = Fetcher(session, semaphore)
        robots = None
        if args.respect_robots:
            robots = RobotsCache(
                session=session,
                semaphore=semaphore,
                user_agent=USER_AGENT,
                timeout=REQUEST_TIMEOUT,
            )

        results = await run_pipeline(
            urls=urls,
            fetcher=fetcher,
            parser=parse,
            worker_count=args.workers,
            max_depth=args.depth,
            link_extractor=extract_links,
            robots=robots,
        )

    print("\nFinal Results:")
    for r in results:
        title = r["data"]["title"] if r.get("data") else "N/A"
        print(f"{r['url']} | Depth: {r.get('depth')} | Status: {r.get('status')} | Title: {title}")

    if args.output:
        fmt = _infer_format(args.output, args.format)
        if fmt == "csv":
            save_csv(results, args.output)
        else:
            save_json(results, args.output)
        print(f"\nSaved results to: {args.output}")

    return 0


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
