#!/usr/bin/env python

# Enable relative import
import os
import sys
import pathlib

if __package__ is None:
    DIR = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(DIR.parent))
    __package__ = DIR.name

# Import packages
from dotenv import load_dotenv
from urllib.parse import quote_plus
from .MongoManager import MongoManager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .routers import (
  api,
  graphs,
)

# Load config from a .env file:
load_dotenv(verbose=True)

# Connect to the database
DB_SRV = bool(int(os.getenv("DB_SRV", "0")))

uri = "{protocol}://{encoded_username}:{encoded_password}@{host}/".format(
  protocol="mongodb+srv" if DB_SRV else "mongodb",
  encoded_username=quote_plus(os.getenv("DB_USERNAME")),
  encoded_password=quote_plus(os.getenv("DB_PASSWORD")),
  host=os.getenv("DB_HOST"),
)
db = MongoManager(
  uri=uri,
  tls=DB_SRV,
  db_name=os.getenv("DB_NAME"),
  coll_name=os.getenv("COLL_NAME"),
)

# Initialize the app (fastapi run)
if __name__ == "src.main":
  app = FastAPI()
  app.mount("/assets", StaticFiles(directory="assets"), name="assets")

  templates = Jinja2Templates(directory="templates")
  app.state.templates = templates
  app.state.db = db  # access using request.app.state.db

  # Add routes (python main.py commandname)
  app.include_router(api.router)
  app.include_router(graphs.router)
