"""
aiodec
======

Decorators for coroutines

"""

import time
import logging
from functools import wraps
from string import Template
import inspect


logger = logging.getLogger(__name__)


def adecorator(
        f=None,
        pre_callback=lambda sig, bound_args: None,
        post_callback=lambda sig, bound_args: None):

    def inner(g):
        # Get the function signature of the wrapped function. We need this
        # in order to obtain all the parameter information.
        sig = inspect.signature(g)

        @wraps(g)
        async def wrapper(*args, **kwargs):
            # Using the actually-provided args, bind them to the signature
            # of the wrapped function
            bound_args = sig.bind(*args, **kwargs)
            # Now fill in the unsupplied parameters with their default
            # values.
            bound_args.apply_defaults()
            pre_callback(sig, bound_args)
            try:
                return await g(*args, **kwargs)
            finally:
                post_callback(sig, bound_args)

        return wrapper

    if f:
        # atimer() was called WITHOUT evaluation, so we must return the
        # actual wrapper function that replaces f.
        return inner(f)
    else:
        # atimer() was called WITH evaluation, so we need to return ANOTHER
        # decorator (that will receive  and wrap function f).
        return inner


def atimer(f=None, message_template='Time taken: $time_ seconds', fmt='%.4g'):
    # Using templates because safe_substitute is awesome.
    tmpl = Template(message_template)

    def pre_callback(sig, bound_args):
        nonlocal t0
        t0 = time.perf_counter()

    def post_callback(sig, bound_args):
        dt = time.perf_counter() - t0
        msg = tmpl.safe_substitute(
            **bound_args.arguments,
            time_=fmt % dt
        )
        logger.info(msg)

    return adecorator(
        f,
        pre_callback=pre_callback,
        post_callback=post_callback
    )
