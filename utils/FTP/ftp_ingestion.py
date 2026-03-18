from datetime import datetime
from typing import List, Callable
from ftp_client import SFTPClient


def list_files_with_metadata(client: SFTPClient, remote_path: str = "."):
    """
    Obtiene lista de ficheros con metadatos (incluye fecha modificación).

    Returns:
        lista de objetos SFTPAttributes
    """
    return client.conn.listdir_attr(remote_path)


def filter_files_by_modification_date(
    files_attr,
    min_datetime: datetime,
    extension: str = None,
) -> List[str]:
    """
    Filtra ficheros por fecha de modificación.

    Args:
        files_attr: resultado de listdir_attr()
        min_datetime: fecha mínima (incremental)
        extension: filtrar por extensión (.csv, .xlsx...)

    Returns:
        lista de nombres de ficheros
    """
    filtered_files = []

    for attr in files_attr:
        file_datetime = datetime.utcfromtimestamp(attr.st_mtime)

        if file_datetime > min_datetime:
            if extension and not attr.filename.endswith(extension):
                continue

            filtered_files.append(attr.filename)

    return filtered_files


def incremental_download(
    client: SFTPClient,
    remote_path: str,
    local_path: str,
    last_processed_datetime: datetime,
    extension: str = None,
) -> List[str]:
    """
    Descarga incremental basada en fecha de modificación.

    Args:
        client: SFTPClient
        remote_path: carpeta remota
        local_path: carpeta local
        last_processed_datetime: última fecha procesada
        extension: filtro opcional

    Returns:
        lista de ficheros descargados
    """
    # Cambiar directorio remoto
    client.conn.cwd(remote_path)

    # Obtener metadatos
    files_attr = list_files_with_metadata(client)

    # Filtrar ficheros nuevos
    files_to_download = filter_files_by_modification_date(
        files_attr,
        min_datetime=last_processed_datetime,
        extension=extension,
    )

    # Descargar
    downloaded = client.download_files(files_to_download, local_path)

    return downloaded
