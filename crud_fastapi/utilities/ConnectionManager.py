from fastapi import WebSocket
from pydantic import BaseModel

class UserWSList(BaseModel):
    user_name: str = ''
    ws: list[int] = []

class WS_Manager:
    def __init__(self):
        self.conns: list[WebSocket] = []
        self.websocket_user_list:dict = {}
        
    async def connect(self, websocket: WebSocket, user: str = None):
        await websocket.accept()
        self.conns.append(websocket)
        if user:
            try:
                self.websocket_user_list[user].user_name = user
                self.websocket_user_list[user].ws.append(id(websocket))
            except KeyError:
                self.websocket_user_list[user] = UserWSList()
                self.websocket_user_list[user].user_name = user
                self.websocket_user_list[user].ws.append(id(websocket))
            finally:
                self.show_count(user)
    def disconnect(self, websocket: WebSocket, user: str = None):
        self.conns.remove(websocket)
        if user:
            self.websocket_user_list[user].ws.remove(id(websocket))
        
    async def broadcast(self, config, user: str = None):
        if user:
            for ws in self.conns:
                if id(ws) in self.websocket_user_list[user].ws:
                    await ws.send_json(config)

        else:
            for ws in self.conns:
                await ws.send_json(config)
                
    def show_count(self, user: str = None):
        print(f'{len( self.websocket_user_list[user].ws)} ws para {user}')
        return len( self.websocket_user_list[user].ws)