import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
import httpx

# Load environment variables from .env
load_dotenv()

app = FastAPI(
    title="CMS0057 FHIR Proxy",
    description="Proxy RESTful endpoints to a HAPI-FHIR server for CMS 0057",
    version="1.0.0"
)

# Base URL of HAPI-FHIR server
FHIR_SERVER_URL = os.getenv("FHIR_SERVER_URL", "http://localhost:8080")

async def proxy_request(method: str, path: str, params=None, json_body=None):
    async with httpx.AsyncClient() as client:
        url = f"{FHIR_SERVER_URL}/{path}"
        response = await client.request(method, url, params=params, json=json_body)
    try:
        content = response.json()
    except ValueError:
        content = response.text
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=content)
    return content

# Generic CRUD endpoints for all FHIR resources
@app.post("/{resource_type}")
async def create_resource(resource_type: str, request: Request):
    body = await request.json()
    return await proxy_request("POST", resource_type, json_body=body)

@app.get("/{resource_type}")
async def search_resource(resource_type: str, request: Request):
    params = list(request.query_params.multi_items())
    return await proxy_request("GET", resource_type, params=params)

@app.get("/{resource_type}/{id}")
async def read_resource(resource_type: str, id: str):
    return await proxy_request("GET", f"{resource_type}/{id}")

@app.put("/{resource_type}/{id}")
async def update_resource(resource_type: str, id: str, request: Request):
    body = await request.json()
    return await proxy_request("PUT", f"{resource_type}/{id}", json_body=body)

@app.delete("/{resource_type}/{id}")
async def delete_resource(resource_type: str, id: str):
    return await proxy_request("DELETE", f"{resource_type}/{id}")

# Generic FHIR type-level operation proxy (e.g. /Patient/$submit-authorization)
@app.post("/{resource_type}/{operation_name}")
async def type_operation(resource_type: str, operation_name: str, request: Request):
    body = await request.json()
    return await proxy_request("POST", f"{resource_type}/{operation_name}", json_body=body)

# Generic FHIR instance-level operation proxy (e.g. /CoverageEligibilityRequest/{id}/$approve)
@app.post("/{resource_type}/{id}/{operation_name}")
async def instance_operation(resource_type: str, id: str, operation_name: str, request: Request):
    body = await request.json()
    return await proxy_request("POST", f"{resource_type}/{id}/{operation_name}", json_body=body)

# FHIR CapabilityStatement (metadata) endpoint
@app.get("/metadata")
async def get_metadata():
    """Proxy the FHIR CapabilityStatement from HAPI-FHIR"""
    return await proxy_request("GET", "metadata")

# CMS 0057 specific operation: evaluate-measure
@app.post("/Measure/{id}/$evaluate-measure")
async def evaluate_measure(id: str, request: Request):
    body = await request.json()
    return await proxy_request("POST", f"Measure/{id}/$evaluate-measure", json_body=body)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)), reload=True)
