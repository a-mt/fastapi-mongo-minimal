from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class CountDocuments(BaseModel):
  """
  Defines the response serializer for the API
  """
  n_documents: int


@router.get("/", tags=["api"])
def home(request: Request) -> CountDocuments:
  """
  Return the number of documents in the current collection
  If empty, adds a sample document
  """
  db = request.app.state.db
  n_documents = db.collection.count_documents({})

  if n_documents == 0:
    db.create_one_document({
      "test": "OK",
    })
  return {"n_documents": n_documents}


@router.get("/users/", tags=["api"])
async def read_users():
    return [
      {"username": "Rick"},
      {"username": "Morty"},
    ]


@router.get("/users/me", tags=["api"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["api"])
async def read_user(username: str):
    return {"username": username}
