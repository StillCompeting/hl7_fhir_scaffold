import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from httpx import AsyncClient
from api.main import app

@pytest.mark.asyncio
async def test_create_and_read_resource(monkeypatch):
    # stub out proxy_request to return a dummy payload
    async def dummy_proxy(method, path, params=None, json_body=None):
        return {"dummy": True, "path": path}
    monkeypatch.setattr("api.main.proxy_request", dummy_proxy)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # test create
        resp = await ac.post("/Patient", json={"resourceType": "Patient"})
        assert resp.status_code == 200
        assert resp.json()["dummy"] is True

        # test read
        resp2 = await ac.get("/Patient/123")
        assert resp2.status_code == 200
        assert resp2.json()["path"] == "Patient/123"

@pytest.mark.asyncio
async def test_evaluate_measure(monkeypatch):
    async def dummy_proxy(method, path, params=None, json_body=None):
        return {"evaluated": True, "id": path.split('/')[1]}
    monkeypatch.setattr("api.main.proxy_request", dummy_proxy)

    measure_id = "test-measure"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            f"/Measure/{measure_id}/$evaluate-measure",
            json={"periodStart": "2020-01-01", "periodEnd": "2020-12-31"}
        )
        assert resp.status_code == 200
        assert resp.json() == {"evaluated": True, "id": measure_id}

@pytest.mark.asyncio
async def test_type_and_instance_operations(monkeypatch):
    async def dummy_proxy(method, path, params=None, json_body=None):
        return {"ok": True, "path": path}
    monkeypatch.setattr("api.main.proxy_request", dummy_proxy)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # type-level operation
        resp = await ac.post("/Patient/$submit-authorization", json={})
        assert resp.status_code == 200
        assert resp.json()["path"] == "Patient/$submit-authorization"

        # instance-level operation
        resp2 = await ac.post("/CoverageEligibilityRequest/456/$approve", json={})
        assert resp2.status_code == 200
        assert resp2.json()["path"] == "CoverageEligibilityRequest/456/$approve"
