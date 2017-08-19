# Web Application that will handle websocket, with write received by Main.py calls, and values pushed to all web clients

from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('../client/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    """On connection event from client print to stdout the connect event and sid of client."""
    print("connect ", sid)

@sio.on('talk_to_mirror', namespace='/chat')
async def message(sid, data):
    """Get message from client and reply with same message to it."""
    print("message: ", data)
    await sio.emit('reply', data=data['data'], skip_sid=True, namespace='/chat')

@sio.on('disconnect request', namespace='/chat')
async def disconnect(sid):
    """Close socket connection for client with specified sid."""
    print('disconnect ', sid)
    await sio.disconnect(sid, namespace='/chat')

@sio.on('msg_to_server', namespace='/chat')
def my_event(sid, data):
    """Get message from client and print to stdout."""
    print(data, sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port=8085)
