import time
import asyncio
from combined_ranklist.app import CombRanklist

# from dotenv import load_dotenv
# from pathlib import Path 
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

from quart import Quart, render_template, jsonify, request

app = Quart(__name__)

@app.route('/')
async def main():
    return await render_template('home.html')

@app.route('/api/v1/generate_standings', methods=["POST"])
async def ok():
    # try:
    if request.method == 'POST':
        _st = time.time()

        data = await request.form
        
        if 'contest_ids_cf' in data:
            data['contest_ids_cf'] = data['contest_ids_cf'].split()

        if 'contest_ids_atc' in data:
            data['contest_ids_atc'] = data['contest_ids_atc'].split()

        if 'contest_ids_vj' in data:
            data['contest_ids_vj'] = data['contest_ids_vj'].split()
            data['contest_ids_vj_passwords'] = data['contest_ids_vj_passwords'].split(' ')

        c_ranks = CombRanklist(**data)

        await c_ranks.make_standings()
        await c_ranks.dump_standings_to_sheet()
        return f'{round(time.time() - _st,2)}', 200
    # except Exception as e:

    #     print('Exception Occured', e)
    #     return 'Something went Wrong.', 500