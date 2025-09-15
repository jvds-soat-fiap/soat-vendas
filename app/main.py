from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.config import LOGGING_CONFIG
from src.adapters.input.api import api_router


API_BASE_URL = '/soat-veiculo/v1'
API_PORT = 8003

app = FastAPI(title='SOAT Veiculo v1.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:{}".format(API_PORT)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)
app.include_router(api_router, prefix=API_BASE_URL)


def startUvicorn():
    import uvicorn

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(message)s'
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run("main:app",host="0.0.0.0", port=API_PORT, reload=True, log_config=LOGGING_CONFIG)

if __name__ == '__main__':
    startUvicorn()
