import logging

class Logger:
    """
    Logger simplificado para ETL/Data Engineering.
    """
    def __init__(self, use_case="", process="", id_process="", flag_test=False):
        self.use_case = use_case
        self.process = process
        self.id_process = id_process
        self.flag_test = flag_test

        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        self.logger = logging.getLogger(process)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def log_metric(self, metric_name, value):
        self.info(f"METRIC - {metric_name}: {value}")

    def log_end(self):
        self.info(f"Process {self.process} finished.")
