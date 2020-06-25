from channels.routing import ProtocolTypeRouter, URLRouter
from app.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})
