class SFTPConnectionError(Exception):
    """Error al conectar con el servidor SFTP"""
    pass


class SFTPFileNotFoundError(Exception):
    """Fichero no encontrado en SFTP"""
    pass


class SFTPDownloadError(Exception):
    """Error durante la descarga"""
    pass
