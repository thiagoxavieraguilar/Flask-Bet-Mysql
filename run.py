from Bet_tx import create_app
from Bet_tx.views import schedule_thread
from asgiref.wsgi import WsgiToAsgi
import uvicorn
import threading


if __name__ == '__main__':
    app = create_app()
    asgi_app = WsgiToAsgi(app)
    schedule_thread = threading.Thread(target=schedule_thread)
    schedule_thread.start()
    uvicorn.run(asgi_app, host='0.0.0.0', port=8080)