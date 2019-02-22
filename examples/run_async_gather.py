import asyncio

import ferien


async def print_wrapper(state_code):
    print("Fetching {}".format(state_code))
    res = await ferien.state_vacations_async(state_code, 2019)
    print("Fetched {}".format(state_code))
    return res


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coros = [
        print_wrapper('HH'),
        print_wrapper('SH'),
        print_wrapper('BE'),
        print_wrapper('BB')
    ]
    loop.run_until_complete(asyncio.gather(*coros))
