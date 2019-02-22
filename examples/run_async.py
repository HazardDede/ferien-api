import asyncio

import ferien


async def main():
    # Get all vacations for all time and states
    print("All vacations:", await ferien.all_vacations_async())

    # Get all vacations for a specific state (in this case Hamburg - HH) ...
    print("All vacations for HH:", await ferien.state_vacations_async('HH'))

    # ... and optionally for a specific year
    print("All vacations for HH in 2019:", await ferien.state_vacations_async('HH', 2019))

    # Fetch all valid states. This one is _NOT_ async
    print("Valid state codes:", ferien.state_codes())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
