class PipelineRunner:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self):
        return self.pipeline.run()
