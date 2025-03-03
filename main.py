from fastapi import FastAPI
from google.cloud import bigquery

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to add security headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

app.add_middleware(SecurityHeadersMiddleware)


# Initialize BigQuery client
client = bigquery.Client()

@app.get("/data")
def get_data():
    query = "SELECT * FROM `datamining-452305.police.processed_calls_2025` LIMIT 100"
    df = client.query(query).to_dataframe()
    return df.to_dict(orient="records")
