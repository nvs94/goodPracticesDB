from ftp_client import SFTPClient, build_filename, default_logger
from datetime import datetime

logger = default_logger()

HOST = "serafin.iberdrola.com"
USER = "your_user"
PASSWORD = "your_password"

DATE = datetime.now().strftime("%Y%m%d")

files = [
    build_filename("GTL_CCH_INDUSTRIALES_", DATE),
    build_filename("GHH_CCH_FACTURADAS_", DATE),
]


def extract_date_from_filename(filename: str):
    # Example: GTL_CCH_INDUSTRIALES_20240101.csv
    date_str = filename.split("_")[-1].split(".")[0]
    return datetime.strptime(date_str, "%Y%m%d")


client = SFTPClient(
    host=HOST,
    username=USER,
    password=PASSWORD,
    logger=logger
)

with client:
    downloaded_files = client.download_files(files, "/tmp")

    # Cleanup old files (older than 7 days)
    client.delete_old_files(
        days=7,
        date_extractor=extract_date_from_filename
    )

print(downloaded_files)
