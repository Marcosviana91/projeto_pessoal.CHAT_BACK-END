# Crud mensageiro com FastApi, TinyDB, WebSockets, Strawberry

## Dependencias para Auth0:
asgiref==3.4.1
cffi==1.14.6
click==8.0.1
cryptography==3.4.7
<!-- fastapi==0.68.0 -->
h11==0.12.0
pycparser==2.20
<!-- pydantic==1.8.2 -->
PyJWT==2.1.0
starlette==0.14.2
typing-extensions==3.10.0.0
<!-- uvicorn==0.15.0 -->
> poetry add asgiref cffi click cryptography h11 pycparser PyJWT starlette typing-extensions

### Retorno:

```JSON
{
    "given_name": "Marcos", 
    "family_name": "Viana",
    "nickname": "marcos.viana.91",
    "name": "Marcos Viana",
    "picture": "https://lh3.googleusercontent.com/a/ACg8ocIlPVkjav-AFn5t57bf5GQvSMlb8d4MykMyVnllTxb4pfEV=s96-c",
    "locale": "pt-BR",
    "updated_at": "2024-03-13T20:10:13.172Z",
    "email": "marcos.viana.91@gmail.com",
    "email_verified": true,
    "iss": "https://dev-jps52bjwplkvzprb.us.auth0.com/",
    "aud": "nEIxbEwCHfGCo6kjGp58u0wRDhofjoQ9",
    "iat": 1710360614,
    "exp": 1710396614,
    "sub": "google-oauth2|111599641520295750253",
    "sid": "goAvH-YZc3S3_HvudexEAtiiU8K_D11n",
    "nonce": "UELLrbvAAGnMz3SNs27U"
}
```