from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/graphs", response_class=HTMLResponse, tags=["html"])
def graphs(request: Request) -> str:
  return request.app.state.templates.TemplateResponse("graphs.html", context={
    "request": request
  })
