import pysftp
import logging
from datetime import datetime, timedelta
from typing import List, Callable, Optional


class SFTPClient:
    """
    SFTP Client listo para producción.

    Funcionalidades:
    - Conexión segura (password o private key)
    - Context manager (uso con `with`)
    - Descarga y subida de ficheros
    - Eliminación de ficheros antiguos (retention)
    - Logging integrado

    Ejemplo de uso:
        with SFTPClient(...) as client:
            client.download_file("file.csv", "/tmp/file.csv")
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: Optional[str] = None,
        port: int = 22,
        private_key_path: Optional[str] = None,
        known_hosts_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Inicializa el cliente SFTP.

        Args:
            host: Dirección del servidor SFTP
            username: Usuario
            password: Password (opcional si se usa key)
            port: Puerto (default 22)
            private_key_path: Ruta a clave privada
            known_hosts_path: Ruta al fichero known_hosts (seguridad)
            logger: Logger opcional
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.private_key_path = private_key_path
        self.known_hosts_path = known_hosts_path
        self.logger = logger or logging.getLogger(__name__)
        self._conn = None  # conexión interna

    # =========================
    # CONEXIÓN
    # =========================

    def connect(self):
        """
        Establece la conexión SFTP.

        Returns:
            self (para permitir uso con context manager)
        """
        cnopts = pysftp.CnOpts()

        # Configuración de seguridad:
        if self.known_hosts_path:
            # ✔ Producción: validar fingerprint del servidor
            cnopts.hostkeys.load(self.known_hosts_path)
        else:
            # ⚠️ Solo para entornos no productivos
            self.logger.warning("Host key verification is disabled")
            cnopts.hostkeys = None

        # Crear conexión
        self._conn = pysftp.Connection(
            host=self.host,
            username=self.username,
            password=self.password,
            private_key=self.private_key_path,
            port=self.port,
            cnopts=cnopts,
        )

        self.logger.info(f"Connected to SFTP server: {self.host}")
        return self

    def close(self):
        """
        Cierra la conexión SFTP si está abierta.
        """
        if self._conn:
            self._conn.close()
            self.logger.info("SFTP connection closed")

    def __enter__(self):
        """
        Permite usar:
            with SFTPClient(...) as client:
        """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cierra la conexión automáticamente al salir del bloque `with`.
        """
        self.close()

    @property
    def conn(self):
        """
        Acceso seguro a la conexión.

        Lanza error si no está inicializada.
        """
        if not self._conn:
            raise Exception("Connection not established. Use 'with client.connect()'")
        return self._conn

    # =========================
    # OPERACIONES BÁSICAS
    # =========================

    def exists(self, remote_path: str) -> bool:
        """
        Comprueba si un fichero existe en el servidor.

        Args:
            remote_path: ruta remota

        Returns:
            True / False
        """
        return self.conn.exists(remote_path)

    def list_files(self, remote_path: str = ".") -> List[str]:
        """
        Lista los ficheros de un directorio remoto.

        Args:
            remote_path: ruta remota

        Returns:
            Lista de nombres de ficheros
        """
        return self.conn.listdir(remote_path)

    def download_file(self, remote_path: str, local_path: str):
        """
        Descarga un fichero del SFTP.

        Args:
            remote_path: fichero en el servidor
            local_path: ruta local destino

        Raises:
            FileNotFoundError: si el fichero no existe
        """
        if not self.exists(remote_path):
            raise FileNotFoundError(f"{remote_path} not found in SFTP")

        self.conn.get(remote_path, local_path)
        self.logger.info(f"Downloaded: {remote_path} -> {local_path}")

    def download_files(self, files: List[str], local_dir: str) -> List[str]:
        """
        Descarga múltiples ficheros.

        Args:
            files: lista de nombres de ficheros
            local_dir: directorio destino

        Returns:
            Lista de rutas locales descargadas
        """
        downloaded = []

        for file in files:
            local_path = f"{local_dir}/{file}"
            self.download_file(file, local_path)
            downloaded.append(local_path)

        return downloaded

    def upload_file(self, local_path: str, remote_path: str):
        """
        Sube un fichero al SFTP.

        Args:
            local_path: fichero local
            remote_path: destino remoto
        """
        self.conn.put(local_path, remote_path)
        self.logger.info(f"Uploaded: {local_path} -> {remote_path}")

    def delete_file(self, remote_path: str):
        """
        Elimina un fichero del servidor.

        Args:
            remote_path: fichero a eliminar
        """
        self.conn.remove(remote_path)
        self.logger.info(f"Deleted: {remote_path}")

    # =========================
    # UTILIDADES AVANZADAS
    # =========================

    def delete_old_files(
        self,
        days: int,
        date_extractor: Callable[[str], datetime],
        remote_path: str = ".",
    ):
        """
        Elimina ficheros antiguos según política de retención.

        Args:
            days: número de días a conservar
            date_extractor: función que extrae fecha desde nombre de fichero
            remote_path: directorio remoto

        Ejemplo date_extractor:
            lambda f: datetime.strptime(f[-12:-4], "%Y%m%d")
        """
        files = self.list_files(remote_path)

        for f in files:
            try:
                file_date = date_extractor(f)

                # Si el fichero es más antiguo que el umbral → borrar
                if file_date + timedelta(days=days) < datetime.now():
                    self.delete_file(f)

            except Exception as e:
                # Si no se puede parsear la fecha → ignorar fichero
                self.logger.warning(f"Skipping file {f}: {str(e)}")

# =========================
# HELPERS
# =========================
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
