import strawberry
from strawberry.fastapi import GraphQLRouter

from fastapi import Depends
from fastapi.requests import Request

from .mutations import Mutation
from .queries import Query

from ..DataBaseManager import DB_Manager



db = DB_Manager()

def getUserIdByAuthId(request: Request) -> int:
    return 1
    # user_id = db.getUserIdByAuthID(auth_id=request.session['userinfo']['sub'])[0]
    return user_id

async def get_context(
    user_id = Depends(getUserIdByAuthId),
):
    return {
        "user_id": user_id,
    }

    
schema = strawberry.Schema(query=Query, mutation=Mutation, )

graphql_app = GraphQLRouter(schema, context_getter=get_context)
# graphql_app = GraphQLRouter(schema)