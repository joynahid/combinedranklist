import time
import asyncio
import json
from combined_ranklist.app import CombRanklist
from quart import render_template, jsonify, request, make_response, websocket

class Manager:
    @staticmethod
    async def showIndex():
        return await render_template("home.html")

    @staticmethod
    async def generateStandings(data):
        try:
            _st = time.time()

            data = json.loads(data)

            if "contest_ids_cf" in data:
                data["contest_ids_cf"] = data["contest_ids_cf"].split()

            if "contest_ids_atc" in data:
                data["contest_ids_atc"] = data["contest_ids_atc"].split()

            if "contest_ids_vj" in data:
                data["contest_ids_vj"] = data["contest_ids_vj"].split()
                data["contest_ids_vj_passwords"] = data[
                    "contest_ids_vj_passwords"
                ].split(" ")

            c_ranks = CombRanklist(**data)

            await c_ranks.make_standings()
            await c_ranks.dump_standings_to_sheet()
            
            await websocket.send(f"Successfully updated in {round(time.time() - _st,2)} seconds")
        except Exception as e:
            await websocket.send("<span style='color:red'>"+str(e)+"</span>")
            await websocket.send("Aborted")