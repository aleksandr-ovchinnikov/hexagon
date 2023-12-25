from fastapi import APIRouter, Depends, status, Request, Header
from fastapi.templating import Jinja2Templates
import re
import requests
import json
import time
import uuid
import os
import hashlib


router = APIRouter(tags=["Frontend"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
