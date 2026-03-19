import time

class DataPipeline:
    """
    End-to-end pipeline orchestration.
    """

    def __init__(self, name, steps, logger=None, metrics=None):
        self.name = name
        self.steps = steps
        self.logger = logger
        self.metrics = metrics

    def run(self):
        data = None
        start_time = time.time()

        if self.logger:
            self.logger.info(f"Pipeline {self.name} started")

        for step in self.steps:
            step_start = time.time()

            if self.logger:
                self.logger.info(f"Step {step.name} started")

            data = step.run(data)

            duration = time.time() - step_start

            if self.metrics:
                self.metrics.log_metric(f"{step.name}_duration", duration)

            if self.logger:
                self.logger.info(f"Step {step.name} finished in {duration:.2f}s")

        total_duration = time.time() - start_time

        if self.metrics:
            self.metrics.log_metric("pipeline_duration", total_duration)

        if self.logger:
            self.logger.info(f"Pipeline {self.name} finished in {total_duration:.2f}s")

        return data
