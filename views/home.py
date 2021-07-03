import json
import random

import fastapi
from fastapi import Form, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from jinja2.exceptions import TemplateNotFound

from api.layout_api import get_layout_content


router = fastapi.APIRouter()
templates = Jinja2Templates('templates')



async def _cookie_handler(content: dict, cookies: dict):
	""" """
	for k,v in cookies.items():
		if k in content.keys():
			if k == 'darkmode':
				if v == 'False':
					v = False
				elif v == 'True':
					v = True

			content.update({k:v})

	return content


async def get_template_content(req: Request):
	"""	"""
	cont = await get_layout_content()
	cont = await _cookie_handler(cont, req.cookies)

	cont.update({"request": req})

	return cont


""" defining any non-notebook /single-slug catches beforehand,
	e.g. contact page
"""
@router.get('/contact', include_in_schema=False)
async def contact(request: Request):
	""" """
	cont = await get_template_content(request)

	return templates.TemplateResponse('home/contact.html', cont)


@router.post('/contact', include_in_schema=False)
async def contact_post(email_address=Form(...), email_message=Form(...)):
	""" todo 
	"""
	print(email_address, email_message) #by <input name="x">
	return {"email_address": email_address, "email_message": email_message}


""" 
"""
@router.get('/', include_in_schema=False)
async def home(request: Request):
	""" """
	cont = await get_template_content(request)

	return templates.TemplateResponse('home/home.html', cont)


@router.get('/{content}', include_in_schema=False)
async def content(request: Request, content: str):
	""" main catching route to /single-slug
		:returns: from templates/blog function
			or -> templates/home/404.html
	"""
	cont = await get_template_content(request)

	try:
		return templates.TemplateResponse(f'blog/{content}.html', cont)
	except TemplateNotFound:
		cont.update({'unavailable_content': content})
		return templates.TemplateResponse(f'shared/404.html', cont)


@router.post('/', include_in_schema=False)
@router.post('/{content}', include_in_schema=False)
async def cookie_post(request: Request, darkmode=Form(...), content:str=''):
	""" """
	print('cookies', request.cookies)
	
	response = RedirectResponse(url=request.url.path, status_code=status.HTTP_303_SEE_OTHER)
	response.set_cookie('hello', 'world')	

	if darkmode == 'darkmode':
		response.set_cookie('darkmode', True)

	if darkmode == 'lightmode':
		response.set_cookie('darkmode', False)

	return response


@router.get('/favicon.ico', include_in_schema=False)
def favicon():
	""" """
	return fastapi.responses.RedirectResponse(url='static/img/favicon.ico')










