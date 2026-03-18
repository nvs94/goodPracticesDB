# ==========================================
# Name: fetch_paginated_data
# Category: utils / api / pagination
# Description: Generic pagination handler with optional parallel fetching
# ==========================================

from typing import Callable, List, Dict, Any, Optional
import concurrent.futures


def fetch_paginated_data(
    fetch_page_fn: Callable[[int], Dict[str, Any]],
    extract_items_fn: Callable[[Dict[str, Any]], List[Dict]],
    get_total_pages_fn: Callable[[Dict[str, Any]], int],
    parallel: bool = True,
    max_workers: int = 5,
) -> List[Dict]:
    """
    Generic function to fetch paginated API data.

    Args:
        fetch_page_fn: Function that retrieves a page given a page number
        extract_items_fn: Function to extract items from API response
        get_total_pages_fn: Function to get total number of pages
        parallel: Whether to fetch pages in parallel
        max_workers: Number of threads for parallel execution

    Returns:
        List[Dict]: Aggregated list of items
    """

    # Fetch first page
    first_page = fetch_page_fn(1)
    if not first_page:
        raise Exception("Failed to fetch first page")

    total_pages = get_total_pages_fn(first_page)
    results = extract_items_fn(first_page)

    if total_pages <= 1:
        return results

    pages = list(range(2, total_pages + 1))

    if not parallel:
        for page in pages:
            response = fetch_page_fn(page)
            if response:
                results.extend(extract_items_fn(response))
        return results

    # Parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_page_fn, page): page for page in pages}

        for future in concurrent.futures.as_completed(futures):
            page = futures[future]
            try:
                response = future.result()
                if response:
                    results.extend(extract_items_fn(response))
            except Exception as e:
                raise Exception(f"Error fetching page {page}: {e}")

    return results

''' ----------------USE EXAMPLE----------------
def fetch_page(page: int):
    endpoint = f"/device?_limit=10000&_page={page}"
    return client.get(endpoint)


def extract_items(response):
    return response.get("items", [])


def get_total_pages(response):
    return response.get("pages", 1)


devices = fetch_paginated_data(
    fetch_page_fn=fetch_page,
    extract_items_fn=extract_items,
    get_total_pages_fn=get_total_pages,
    parallel=True,
    max_workers=5,
)
'''
