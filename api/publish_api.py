import os
import datetime

import fastapi
from fastapi import File, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

from .auth_api import oauth2_scheme


router = fastapi.APIRouter()

PUB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'blog')
IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'imgs')



class Publishment(BaseModel):
	name: str
	content: str



async def add_publishment(name: str, content: str) -> Publishment:
	""" """
	extends = "{% extends 'shared/layout.html' %}\n\n"
	start_block = '{% block content %}\n\n'
	end_block = '\n\n{% endblock %}'
	content = f'{extends}{start_block}{content}{end_block}'

	with open(os.path.join(PUB_PATH, f'{name}.html'), 'w') as pf:
		pf.write(content)

	pub = Publishment(
		name=name,
		content=content,
		)

	return pub


@router.post('/api/publishment', name='add_pub', status_code=201, response_model=Publishment, dependencies=[Depends(oauth2_scheme)]) # if ok status_code 200 -> 201, if not, it's handled in the ValidationError
async def publishment_post(pub_submittal: Publishment):
	""" Add Pub 
	"""
	n = pub_submittal.name
	c = pub_submittal.content

	return await add_publishment(n, c)


@router.post('/api/image', name='add_img', status_code=201, dependencies=[Depends(oauth2_scheme)])
async def image_post(file: UploadFile = File(...)):
	""" Add Img 
	"""
	contents = await file.read()	
	with open(os.path.join(IMG_PATH, file.filename), 'wb') as f:
		f.write(contents)

	return {"filename": file.filename}



@router.get('/api/publishments', dependencies=[Depends(oauth2_scheme)])
async def publishments_get() -> list:
	""" Publishments Get 
	"""
	pub_names = os.listdir(PUB_PATH)
	pub_data = []
	for p in pub_names:
		mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(PUB_PATH, p)))
		pub_data.append({'pub_name': p, 'mod_date': mod_date})

	return pub_data


@router.get('/api/images', dependencies=[Depends(oauth2_scheme)])
async def images_get() -> list:
	""" Images Get 
	"""
	img_names = os.listdir(IMG_PATH)
	img_data = []
	for n in img_names:
		mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(IMG_PATH, n)))
		img_data.append({'img_name': n, 'mod_date': mod_date})

	return img_data


@router.delete('/api/publishment/{pub_name}', dependencies=[Depends(oauth2_scheme)])
async def publishment_delete(pub_name: str):
	""" Publishment Delete 
	"""
	pub_names = os.listdir(PUB_PATH)
	if pub_name in pub_names:
		os.remove(os.path.join(PUB_PATH, pub_name))

		return {'pub_name': pub_name}









