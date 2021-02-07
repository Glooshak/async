import asyncio
from time import time

import aiohttp


# Запись файла работает синхронно - вообще это плохая практика смешивать синхронные функции и асинхронные
def write_image(data):
    filename = f'file-{int(time() * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main():
    url = 'https://loremflickr.com/320/240'
    tasks = list()

    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
