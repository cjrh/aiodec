def test_timer_default():

    loop = get_loop()

    @timer.atimer
    async def f(x):
        await asyncio.sleep(0.01)
        return x + 1

    result = loop.run_until_complete(f(3))
    assert result == 4


def test_timer_custom():

    loop = get_loop()

    @timer.atimer(message_template='Blah $_time s')
    async def f(x):
        await asyncio.sleep(0.01)
        return x + 1

    result = loop.run_until_complete(f(3))
    assert result == 4


def test_timer_invalid_template():

    loop = get_loop()

    @timer.atimer(message_template='Blah')
    async def f(x):
        await asyncio.sleep(0.01)
        return x + 1

    result = loop.run_until_complete(f(3))
    assert result == 4


def test_timer_invalid_raise():

    loop = get_loop()

    @timer.atimer(message_template='RuntimeError test took: $time_')
    async def f():
        await asyncio.sleep(0.01)
        raise RuntimeError('blah')

    with pytest.raises(RuntimeError):
        loop.run_until_complete(f())


def test_timer_moar_template(caplog):

    loop = get_loop()

    @timer.atimer(message_template='abc=$abc ddd=$ddd time=$time_ secs')
    async def f(abc, ddd=123):
        await asyncio.sleep(0.01)
        return 'ok'

    result = loop.run_until_complete(f(3))
    assert result == 'ok'
    for r in caplog.records:
        if 'abc=3 ddd=123 time=' in r.message:
            break
    else:
        assert False

