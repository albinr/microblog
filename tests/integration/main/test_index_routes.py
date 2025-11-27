"""
Test routes for routes for authorizing users, app/main/routes
"""
# pylint: disable=redefined-outer-name,unused-argument

def test_index_route_to_login(client):
    """
    Test redirect to login when go to index and not authorized
    """
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data
    assert b"Sign In" in response.data



def test_index_post(client, user_post_response, user_dict):
    """
    Test redirect to login when go to index and not authorized
    """
    response = user_post_response
    assert b"Say something" in response.data
    assert b"Submit" in response.data
    assert response.status_code == 200
    assert str.encode("Hi, " + user_dict["username"]) in response.data
    assert b"This is my first post" in response.data
    assert b"Your post is now live" in response.data
    assert b"Submit" in response.data


def test_version_route(client, monkeypatch):
    """
    Test version route returns JSON with version info
    """
    monkeypatch.delenv("APP_VERSION", raising=False)
    response = client.get("/version")
    assert response.status_code == 200
    assert response.content_type == "application/json"

    json_data = response.get_json()
    assert "version" in json_data
    assert json_data["version"] == "unknown"  # Default when APP_VERSION not set


def test_version_route_with_app_version(client, monkeypatch):
    """
    Test version route with APP_VERSION environment variable set
    """
    monkeypatch.setenv("APP_VERSION", "v1.2.3")
    response = client.get("/version")
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["version"] == "v1.2.3"
