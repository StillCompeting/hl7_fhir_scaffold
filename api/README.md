# CMS0057 FHIR Proxy API

This FastAPI application proxies RESTful requests to a HAPI-FHIR server, providing CRUD operations for all FHIR resources plus the CMS 0057 `$evaluate-measure` operation.

## Setup

1. Create a `.env` file in the project root:
   ```
   FHIR_SERVER_URL=http://localhost:8080
   PORT=8001
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn api.main:app --reload
   ```

## Endpoints

- POST `/{resource_type}`: Create a resource
- GET `/{resource_type}`: Search resources
- GET `/{resource_type}/{id}`: Read a resource by ID
- PUT `/{resource_type}/{id}`: Update a resource by ID
- DELETE `/{resource_type}/{id}`: Delete a resource by ID
- POST `/Measure/{id}/$evaluate-measure`: Evaluate a measure for CMS 0057
- POST `/{resource_type}/{operation_name}`: Execute any type-level FHIR operation (e.g. `Patient/$submit-authorization`)
- POST `/{resource_type}/{id}/{operation_name}`: Execute any instance-level FHIR operation (e.g. `CoverageEligibilityRequest/{id}/$approve`)

## Notes
- Ensure your HAPI-FHIR server is running and accessible at the URL in `.env`
- Custom operations beyond evaluate-measure can be added similarly

## Testing

Automated tests using pytest are in `tests/test_api.py`.
Install pytest if needed:
```bash
pip install pytest
```
Run tests:
```bash
pytest -q
```
