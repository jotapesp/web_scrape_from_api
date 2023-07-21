from asyncio import ensure_future, gather, get_event_loop, wait
from aiohttp import ClientSession
from json import load, loads, dump, dumps
import time

urls = ['http://127.0.0.1:8000/usuario',
        'http://127.0.0.1:8000/dados']

async def fetch(session, url):
    async with session.get(url) as response:
        if response.ok:
            return await response.json()
        else:
            return None

async def get_data():
    async with ClientSession() as session:
        task = ensure_future(fetch(session, urls[1]))
        response = await gather(task)
        resp = response[0]
        print(f"""  total de usuarios = {resp["total_usuarios"]}
    media de idade = {resp["media_idade"]}
    mulhers = {resp["mulheres"]}
    homens = {resp["homens"]}
    não-binario/outros = {resp["nao-binario_outros"]}""")

async def get_users():
    tasks = []
    async with ClientSession() as session:
        for user_id in range(1, 21):
            task = ensure_future(fetch(session,
                                        urls[0] + f'/{user_id}'))
            tasks.append(task)

        responses = await gather(*tasks)
        [print(resp["nome"], resp["nascimento"], resp["cpf"], resp["genero"]) for resp in responses if resp]

if __name__ == '__main__':
    start = time.time()
    loop = get_event_loop()
    f1 = ensure_future(get_users())
    f2 = ensure_future(get_data())
    loop.run_until_complete(wait([f1, f2]))
    end = time.time()
    print()
    print(end - start, "segundos")
