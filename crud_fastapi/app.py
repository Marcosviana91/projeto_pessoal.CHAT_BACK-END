from secrets import token_hex

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles  # servidor de arquivos estáticos
from fastapi.templating import Jinja2Templates  # templates

# importar as variáveis de ambiante
from pydantic_settings import BaseSettings, SettingsConfigDict

from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth

from urllib.parse import quote_plus, urlencode

from crud_fastapi.utilities.DataBaseManager import DB_Manager, User
from crud_fastapi.utilities.ConnectionManager import WS_Manager
from crud_fastapi.utilities.GraphQL import graphql_app
# from crud_fastapi.utilities.VerifyToken import VerifyToken
from crud_fastapi.utilities.templatesRender import Render

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]


# variáveis de ambiante


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env'
    )
    DOMAIN: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    SECRET_KEY: str
    AUDIENCE: str = ''
    FRONT_END_HOME: str


settings = Settings()
oauth = OAuth()
oauth.register(
    'auth0',
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid profile email'
    },
    server_metadata_url=f'https://{
        settings.DOMAIN}/.well-known/openid-configuration'
)

db = DB_Manager()
websocket_list = WS_Manager()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
    # exposed_headers= HEADERS,
)


app.include_router(graphql_app, prefix='/graphql', )


# montando a pasta de arquivos estáticos
app.mount(
    '/static_build', StaticFiles(directory='crud_fastapi/templates/build'), name='static_build'
)


@app.get('/', )
def handleRoot(request: Request):
    return HTMLResponse(content=Render('index.html'), status_code=200)


@app.get('/chat')
async def handleRoot(request: Request):
    if (
        not 'id_token' in request.session
    ):
        return await oauth.auth0.authorize_redirect(
            request,
            redirect_uri=request.url_for('callback'),
            audience=settings.AUDIENCE,
        )
    # Verificar se o usuário ja está registrado
    # print(request.session['userinfo']['name'])
    # print(request.session['userinfo']['picture'])
    # print(request.session['userinfo']['email'])
    # print(request.session['userinfo']['sub'])
    user_id = db.getUserIdByAuthID(request.session['userinfo']['sub'])
    if (len(user_id) == 0):
        print(db.createNewUser(
            auth_id=request.session['userinfo']['sub'],
            name=request.session['userinfo']['name'],
            photo=request.session['userinfo']['picture'],
            email=request.session['userinfo']['email'],
            contact_list=[]
        ))
    user_id = db.getUserIdByAuthID(request.session['userinfo']['sub'])[0]
    user_id = 1
    
    authToken = token_hex(16)
    headers = {
        "set-cookie": f"authToken={authToken}"
    }

    return HTMLResponse(headers=headers, content=Render('index.html', user_id=user_id), status_code=200)


@app.get('/login')
async def login(request: Request):
    if (
        not 'id_token' in request.session
    ):  # it could be userinfo instead of id_token
        return await oauth.auth0.authorize_redirect(
            request,
            redirect_uri=request.url_for('callback'),
            audience=settings.AUDIENCE,
        )
    return RedirectResponse('/chat')


@app.get('/callback')
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    request.session['access_token'] = token['access_token']
    request.session['id_token'] = token['id_token']
    request.session['userinfo'] = token['userinfo']
    return RedirectResponse('/chat')


@app.get('/logout')
async def logout(request: Request):
    response = RedirectResponse(
        url='https://'
        + settings.DOMAIN
        + '/v2/logout?'
        + urlencode(
            {
                'returnTo': settings.FRONT_END_HOME,
                'client_id': settings.CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )
    request.session.clear()
    return response


@app.websocket("/ws/{user_name}")
async def websocket_endpoint(websocket: WebSocket, user_name: str):
    print('WebSoket with user:', db.getUserIdByAuthID(websocket.session['userinfo']['sub'])[0])
    await websocket_list.connect(websocket, user_name.lower())
    try:
        while True:
            data:dict = await websocket.receive_json()
            try: 
                authToken = data.get("connectionParams").get("authToken")
                print('Token de autenticação WS: ', authToken, (authToken == websocket.cookies['authToken']))
            except:
                print("Payload: ", data)
                websocket.send_json(data)
            await websocket_list.broadcast(data, user_name.lower())
    except WebSocketDisconnect:
        websocket_list.disconnect(websocket, user_name.lower())
    return None


@app.get('/newuser')
async def createNewUser():
    from .utilities.populate import run
    run()
    return {'message': 'deu bom'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
