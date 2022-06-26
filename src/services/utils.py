import asyncio
import time
from functools import wraps, partial


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


@async_wrap
def test_async(delay):
    time.sleep(delay)
    return 'I slept asynchronously'


async def test():
    print("Hello")
    await test_async(2)
    print("world")

if __name__ == "__main__":
    asyncio.run(test())
