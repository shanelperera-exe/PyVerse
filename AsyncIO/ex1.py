import time


def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


def main():
    result1 = fetch_data(1)
    print("Fetch 1 fully completed")
    result2 = fetch_data(2)
    print("Fetch 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = main()
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")

# Full explanation:
# In this code, the fetch_data function uses time.sleep, which blocks the execution for the
# specified duration. When we call fetch_data(1), it will block for 1 second, and only after it completes,
# fetch_data(2) will be called, blocking for an additional 2 seconds. Therefore, the total execution time
# will be approximately 3 seconds, demonstrating that the tasks are running sequentially rather than concurrently.