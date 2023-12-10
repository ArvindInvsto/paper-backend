from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import BrokerageApi

from priceDataframe import priceDataframe_api
from priceDatabase import priceDatabase_api


app = FastAPI(title="SHARKSIGMA-PAPER-BROKERAGE & DATA", reload = False)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def startup_event():
#     await on_startup()


app.include_router(BrokerageApi.router)


app.include_router(priceDatabase_api)
app.include_router(priceDataframe_api)

