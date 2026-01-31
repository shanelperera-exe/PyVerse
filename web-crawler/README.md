# Async Web Crawler (Phase 3)

This is a small async web crawler built with `aiohttp` + `asyncio`.

## Setup

```bash
cd /home/shanelperera/PyVerse/web-crawler
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run (defaults)

Runs with a built-in seed URL list and prints results.

```bash
python main.py
```

## CLI usage

### Crawl specific URLs

```bash
python main.py --url https://example.com --url https://www.python.org
```

### Read seed URLs from a file

```bash
python main.py --urls-file seeds.txt
```

`seeds.txt` format: one URL per line. Lines starting with `#` are ignored.

### Depth crawling

Depth `0` means only the seed URLs.

```bash
python main.py --url https://example.com --depth 1
```

### Worker count

```bash
python main.py --url https://example.com --workers 10
```

### Respect robots.txt (optional)

```bash
python main.py --url https://example.com --respect-robots
```

If `robots.txt` cannot be fetched, the crawler **fails open** (does not block).

## Persist results (JSON/CSV)

### JSON

```bash
python main.py --url https://example.com --output results.json
```

### CSV

```bash
python main.py --url https://example.com --output results.csv
```

You can force the format regardless of extension:

```bash
python main.py --url https://example.com --output out.data --format json
```
