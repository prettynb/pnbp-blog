import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from api import publish_api, auth_api, layout_api
from views import home



api = fastapi.FastAPI()



def configure_routing():
	""" mounting routes 
	"""
	api.mount('/static', StaticFiles(directory='static'), name='static') 
	api.include_router(home.router)
	api.include_router(publish_api.router)
	api.include_router(auth_api.router)
	api.include_router(layout_api.router)


def configure():
	""" main 
	"""
	configure_routing()
	register_tortoise(
		api,
		db_url='sqlite://db.sqlite3',
		modules={'models': ['api.auth_api']},
		generate_schemas=True,
		add_exception_handlers=True
		)





if __name__ == '__main__':
	configure()
	uvicorn.run(api, port=8000, host='127.0.0.1')
else:
	configure() # <- a production necessary thing
	# uvicorn main:api <- run server




