"""
До python 3.5 использовали декоратор @asyncio.coroutine для обозначения корутины, и yield from для вызова подгенератора,
после для обозначении корутины появилось ключевое слово async def, а для подгенератора await
"""


import asyncio
from time import time


async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)


async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f'{count} seconds have passed.')
        count += 1
        await asyncio.sleep(1)


async def main():
    # В python 3.6 вместо ensure_future начали ипсользовать create_task
    task1 = asyncio.create_task(print_nums())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    # В python 3.7 вместо этих трех строчек начали использовать run()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    asyncio.run(main())
