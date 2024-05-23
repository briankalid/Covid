from fastapi import APIRouter, Request, BackgroundTasks, UploadFile, File, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from typing import List

from core.settings import settings
from common.responses import EnvelopeResponse
from schemas.file_filter import FileFilterSchema
from services.aws_s3 import s3controller

router = APIRouter(prefix="/file")
templates = Jinja2Templates(directory=f"{settings.BASE_DIR}/templates")


@router.get("/file_form")
def file_form(request:Request):

    return templates.TemplateResponse(
        "file_input_form.html",
        {
            "request": request,
            "countries": settings.COUNTRIES
        }
    )

@router.post("/file_upload")
async def file_upload(file: UploadFile = File(...), country: str = Form(...), year: int = Form(...), background_tasks:BackgroundTasks = BackgroundTasks()):
    # print(file)
    print("income file")
    # print(file.tempdir)
    s3controller.upload_file(file, country, year)
    return EnvelopeResponse(status_code=200)
    # s3controller.upload_file(file,country)


@router.post("/file_exist")
def validate_file_exist(country: str = Form(...), year: int = Form(...)):
    bucket = f"{country.lower()}-bucket-covidkalid"
    filename = f"{country}_{year}.csv"
    exist_file = s3controller.file_exist(bucket, filename)
    return EnvelopeResponse(status_code=200, data=exist_file)

@router.get("/list")
def get_list_files(request: Request, query_params: FileFilterSchema = Depends()):
    files = s3controller.get_list_files_by_filter(query_params)
    return files
    # for country in settings.COUNTRIES:
    #     bucket = f"{country.lower()}-bucket"

@router.get("/repository")
def get_repository(request: Request):
    return templates.TemplateResponse(
        "repository.html",
        {
            "request": request,
            "countries": settings.COUNTRIES
        }
    )

@router.get("/download")
def get_repository(bucket: str, key: str):
    file = s3controller.get_objects(bucket,key)
    return StreamingResponse(content=iter([file]), media_type='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={key}"})