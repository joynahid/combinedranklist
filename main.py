from quart import Quart, request, websocket, copy_current_websocket_context
from manager import Manager
import json
import asyncio

app = Quart(__name__)


@app.route("/")
async def index():
    return await Manager.showIndex()


@app.route("/api/v1/generate_combined_standings", methods=["POST"])
async def genStandings():
    return await Manager.generateStandings(request)

@app.websocket("/ws")
async def ws():
    try:
        data = await websocket.receive()
        await copy_current_websocket_context(Manager.generateStandings)(data)
    except Exception as e:
        print(e)
        pass