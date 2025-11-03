from app import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    js = r.get_json()
    assert js["status"] == "ok"
    assert js["service"] == "feather-backend"
