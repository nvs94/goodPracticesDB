def build_filename(prefix: str, date: str, extension: str = "csv") -> str:
    """
    Construye nombres de fichero dinámicos.

    Ejemplo:
        build_filename("file_", "20240101")
        → file_20240101.csv
    """
    return f"{prefix}{date}.{extension}"


def default_logger(name: str = "sftp_client") -> logging.Logger:
    """
    Crea un logger estándar reutilizable.

    Returns:
        Logger configurado con formato simple
    """
    logger = logging.getLogger(name)

    # Evita duplicar handlers si ya existe
    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
