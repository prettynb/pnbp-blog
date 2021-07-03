import uuid 

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from passlib.hash import bcrypt

import jwt

from decouple import config



router = APIRouter()

JWT_SECRET = config('JWT_SECRET')
JWT_ALGO = config('JWT_ALGO')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/token')
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)



class User(Model):
	""" """
	id = fields.IntField(pk=True)
	username = fields.CharField(max_length=50, unique=True)
	password_hash = fields.CharField(max_length=128)
	tok_uuid = fields.TextField(default=str(uuid.uuid4()))

	def verify_password(self, password):
		""" """
		return bcrypt.verify(password, self.password_hash)


class Password(Model):
	""" """
	password_hash = fields.CharField(max_length=128)



User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

PasswordIn_Pydantic = pydantic_model_creator(Password, name='PasswordIn', exclude_readonly=True)



async def get_optional_user(token: str = Depends(optional_oauth2_scheme)):
	""" bypassing my own HTTPException handling ->
		providing access to optional Depends 
	"""
	try:
		# without proper Bearer token, token is None
		# print(token)
		user = await get_current_user(token)
	except:
		# -> fail quietly
		user = None

	return user

@router.post('/api/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic, curr_user: User_Pydantic = Depends(get_optional_user)):
	""" Create User 
	"""
	# print(curr_user)

	root_user = await User.filter(id=1)

	if root_user:
		# only allowing our init generated root user
		# without creds 
		if not curr_user:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot access.")
		# for user creation
		if not curr_user.id == 1:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed.")

	user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
	await user_obj.save()
	return await User_Pydantic.from_tortoise_orm(user_obj)



async def authenticate_user(username: str, password: str):
	""" """
	user = await User.get(username=username)
	if not user:
		return False
	if not user.verify_password(password=password):
		return False
	return user

@router.post('/api/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
	""" Generate Token 
	"""
	user = await authenticate_user(username=form_data.username, password=form_data.password)
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

	user_obj = await User_Pydantic.from_tortoise_orm(user)

	new_uuid = str(uuid.uuid4())
	await User.filter(id=user_obj.id).update(**{'tok_uuid': new_uuid})

	payload = user_obj.dict().copy()
	del payload['password_hash'] # <- you don't want your password hash in the payload
	payload['tok_uuid'] = new_uuid

	token = jwt.encode(payload=payload, key=JWT_SECRET)

	return {'access_token': token, 'token_type': 'bearer'}



async def get_current_user(token: str = Depends(oauth2_scheme)):
	""" """
	try:
		payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
		user = await User.get(id=payload.get('id'))

	except:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

	return await User_Pydantic.from_tortoise_orm(user) # convert to pydantic, user isnt being passed directly, token is being passed

@router.get('/api/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
	""" Get User 
	"""
	payload = user.dict().copy()
	payload['password_hash'] = '' 	# don't include these
	payload['tok_uuid'] = ''		# back to user here

	return payload


@router.post('/api/users/me', response_model=User_Pydantic)
async def reset_password(password: PasswordIn_Pydantic, user: User_Pydantic = Depends(get_current_user)):
	""" Reset Password 
	"""

	password_hash = password.dict()['password_hash']
	curr_id = user.dict()['id']

	try:
		user = await User.filter(id=curr_id).first()
		_out = {'password_hash': bcrypt.hash(password_hash)}
		await user.update_from_dict(_out).save()

	except:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='failed')

	return await User_Pydantic.from_queryset_single(User.get(id=curr_id))



@router.get('/api')
async def api_index(token: str = Depends(oauth2_scheme)):
	""" """
	return {'the_token': token}









