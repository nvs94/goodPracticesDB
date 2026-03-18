from api_client import APIClient
from api_pipeline import APIPipeline
from auth import BearerTokenAuth
from state_manager import FileStateManager
from storage_adls import ADLSClient

client = APIClient(
    base_url="https://api.example.com",
    auth=BearerTokenAuth("your_token")
)

state = FileStateManager("/tmp/api_state.txt")

adls = ADLSClient(
    account_name="storage",
    file_system="landing",
    credential="secret"
)

pipeline = APIPipeline(
    client=client,
    state_manager=state,
    storage_client=adls,
    endpoint="/data",
    incremental_field="updated_at",
    max_workers=8
)

pipeline.run()
