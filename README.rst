.. image:: https://img.shields.io/badge/stdlib--only-yes-green.svg
    :target: https://img.shields.io/badge/stdlib--only-yes-green.svg

.. image:: https://travis-ci.org/cjrh/aiodec.svg?branch=master
    :target: https://travis-ci.org/cjrh/aiodec

.. image:: https://coveralls.io/repos/github/cjrh/aiodec/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/aiodec?branch=master

.. image:: https://img.shields.io/pypi/pyversions/aiodec.svg
    :target: https://pypi.python.org/pypi/aiodec

.. image:: https://img.shields.io/github/tag/cjrh/aiodec.svg
    :target: https://img.shields.io/github/tag/cjrh/aiodec.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20aiodec-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20aiodec-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/aiodec.svg
    :target: https://img.shields.io/pypi/v/aiodec.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/

aiodec
======

*Decorators for asyncio*

.. contents::

astopwatch
----------

The ``astopwatch`` decorator is used in the following way:

.. code-block:: python

    from aiodec import astopwatch

    @astopwatch
    async def blah(x, y):
        return x + y

What does it do? This simple decorator will emit logs with the following message::

    INFO:aiodec:Time taken: 0.0003 seconds


Not terribly special. Yet. You can also customize the log message:

.. code-block:: python

    from aiodec import astopwatch

    @astopwatch(message_template='Time cost was $time_ sec', fmt='%.1g')
    async def blah(x, y):
        return x + y

This outputs log messages with the following message::

    INFO:aiodec:Time taken: 3e-4 seconds


Two things: first, the template parameter used for the time cost is called
``$time_``; second, you can customize the formatting of the seconds value.
However, it can also do something a lot more interesting: it can include
parameters from the wrapped function in the message:

.. code-block:: python

    from aiodec import astopwatch

    @astopwatch(message_template='x=$x y=$y | $time_ seconds')
    async def blah(x, y=2):
        return x + y


    loop.run_until_complete(blah(1))

This outputs log messages with the following message::

    INFO:aiodec:x=1 y=2 | 0.0003 seconds


Magic! Note that positional args and keyword args and default values
are all handled correctly.

As you saw earlier, in addition to the function parameters, the special
``$time_`` parameter will also be available. The other extra fields are:

- ``$name_``, which contains the ``__name__`` of the wrapped function, and
- ``$qualname_``, which contains the ``__qualname__`` of the wrapped function.

These three template parameters have a trailing underscore, to avoid collisions
with any parameter names.
