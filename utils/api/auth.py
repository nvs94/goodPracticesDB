# ==========================================
# Name: get_bearer_token
# Category: utils / api / auth
# ==========================================

def get_bearer_token(client: BaseAPIClient, username: str, password: str) -> str:
    response = client.post(
        "/admin/login",
        data={"username": username, "password": password},
    )

    if not response or "token" not in response:
        raise Exception("Failed to retrieve token")

    return response["token"]
