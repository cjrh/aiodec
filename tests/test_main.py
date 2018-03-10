import logging
import asyncio
import pytest
from aiodec import astopwatch


logging.basicConfig(level='DEBUG')


def get_loop():
    return asyncio.get_event_loop()


def test_timer_default():

    loop = get_loop()

    @astopwatch
    async def f(x):
        await asyncio.sleep(0.01)
        return x + 1

    result = loop.run_until_complete(f(3))
    assert result == 4


def test_timer_custom():

    loop = get_loop()

    @astopwatch(message_template='Blah $_time s')
    async def f(x):
        await asyncio.sleep(0.01)
        return x + 1

    result = loop.run_until_complete(f(3))
    assert result == 4


def test_timer_invalid_template():

    loop = get_loop()

    @astopwatch(message_template='Blah')
    async def f(x):
        await asyncio.sleep(0.01)
        return x + 1

    result = loop.run_until_complete(f(3))
    assert result == 4


def test_timer_invalid_raise():

    loop = get_loop()

    @astopwatch(message_template='RuntimeError test took: $time_')
    async def f():
        await asyncio.sleep(0.01)
        raise RuntimeError('blah')

    with pytest.raises(RuntimeError):
        loop.run_until_complete(f())


def test_timer_moar_template(caplog):

    loop = get_loop()

    # Observe: the message template is going to include parameter
    # values from the wrapped function.
    @astopwatch(message_template='abc=$abc ddd=$ddd time=$time_ secs')
    async def f(abc, ddd=123):
        await asyncio.sleep(0.01)
        return 'ok'

    result = loop.run_until_complete(f(3))
    assert result == 'ok'
    expected_fragment = 'abc=3 ddd=123 time='
    assert any(expected_fragment in r.message for r in caplog.records)
