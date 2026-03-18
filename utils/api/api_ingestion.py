from typing import List, Dict, Callable


def paginate(
    client,
    endpoint: str,
    params: Dict,
    page_param: str = "page",
    data_key: str = "data",
    max_pages: int = 1000,
) -> List[Dict]:
    """
    Manejo genérico de paginación por número de página.
    """

    results = []
    page = 1

    while page <= max_pages:
        params[page_param] = page

        response = client.get(endpoint, params=params)

        data = response.get(data_key, [])

        if not data:
            break

        results.extend(data)
        page += 1

    return results


def incremental_filter(
    records: List[Dict],
    field: str,
    last_value,
) -> List[Dict]:
    """
    Filtra registros incrementalmente.
    """
    return [r for r in records if r.get(field) and r[field] > last_value]
