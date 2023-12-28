# Pharmacies API

## Dependencies
aiosqlite==0.19.0  
annotated-types==0.6.0  
anyio==4.2.0  
certifi==2023.11.17  
click==8.1.7  
coverage==7.4.0  
databases==0.8.0  
fastapi==0.108.0  
greenlet==3.0.3  
h11==0.14.0  
httpcore==1.0.2  
httpx==0.26.0  
idna==3.6  
pydantic==2.5.3  
pydantic_core==2.14.6  
sniffio==1.3.0  
SQLAlchemy==1.4.50  
starlette==0.32.0.post1  
typing_extensions==4.9.0  
uvicorn==0.25.0  

### Running Locally
Install dependencies: 
```bash
pip install -r requirements.txt
```
Run the application: 
```bash
python3 main.py
```

### Running tests
```bash
python -m coverage run -m unittest  test_main.py
```
```bash
python3 -m coverage report -m
```
```bash
Name           Stmts   Miss  Cover   Missing
--------------------------------------------
main.py           94     16    83%   83-89, 92-98, 120, 122, 124, 128, 143, 145, 149, 168, 170, 193
test_main.py      19      1    95%   40
--------------------------------------------
TOTAL            113     17    85%
```

### Authentication
This API requires two types of authentication:

Bearer Token (OAuth2): Include the Authorization header with the Bearer token.
API Key: Include the Api-Key header with the API key.

## Endpoints

### `/patients`

- **Method:** `GET`
- **Description:** Retrieve a list of patients.
- **Query Parameters:**
  - `first_name`: Filter by first name.
  - `last_name`: Filter by last name.
  - `date_of_birth`: Filter by date of birth.

Example for all:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/patients' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer token_de_autorizacao_fixo' \
  -H 'Api-Key: chave_de_api_fixa'
```

Example for filter:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/patients?first_name=JOANA&last_name=SILVA' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer token_de_autorizacao_fixo' \
  -H 'Api-Key: chave_de_api_fixa'
```

### `/pharmacies`
Method: GET
Description: Retrieve a list of pharmacies.
Query Parameters:
name: Filter by pharmacy name.
city: Filter by city.

Example for all:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/pharmacies' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer token_de_autorizacao_fixo' \
  -H 'Api-Key: chave_de_api_fixa'
```

Example for filter:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/pharmacies?name=DROGAO%20SUPER&city=LIMEIRA' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer token_de_autorizacao_fixo' \
  -H 'Api-Key: chave_de_api_fixa'
```

### `/transactions`
Method: GET
Description: Retrieve a list of transactions.
Query Parameters:
patient_uuid: Filter by patient UUID.
pharmacy_uuid: Filter by pharmacy UUID.

Example for all:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/transactions' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer token_de_autorizacao_fixo' \
  -H 'Api-Key: chave_de_api_fixa'
```

Example for filter:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/transactions?patient_uuid=PATIENT0027&pharmacy_uuid=PHARM0009' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer token_de_autorizacao_fixo' \
  -H 'Api-Key: chave_de_api_fixa'
```

### Contributing
If you'd like to contribute to this project, please fork the repository and create a pull request.

### License
This project is licensed under the GPLv3 License.
