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
from inspect import Signature
from typing import Callable, Optional, Mapping, Any

__version__ = '2018.10.1'

logger = logging.getLogger(__name__)
Callback = Callable[[Signature, Mapping[str, Any]], None]


def adecorator(
        f=None,
        pre_callback: Optional[Callback] = None,
        post_callback: Optional[Callback]= None):

    def inner(g):

        @wraps(g)
        async def wrapper(*args, **kwargs):
            # Get the function signature of the wrapped function. We need this
            # in order to obtain all the parameter information.
            template_parameters = dict(name_=g.__name__, qualname_=g.__qualname__)
            sig = inspect.signature(g)

            # Using the actually-provided args, bind them to the signature
            # of the wrapped function
            bound_args = sig.bind(*args, **kwargs)
            
            # Now fill in the unsupplied parameters with their default
            # values.
            bound_args.apply_defaults()
            template_parameters.update(bound_args.arguments)
            pre_callback and pre_callback(sig, template_parameters)
            try:
                return await g(*args, **kwargs)
            finally:
                post_callback and post_callback(sig, template_parameters)

        return wrapper

    if f:
        # astopwatch() was called WITHOUT evaluation, so we must return the
        # actual wrapper function that replaces f.
        return inner(f)
    else:
        # astopwatch() was called WITH evaluation, so we need to return ANOTHER
        # decorator (that will receive  and wrap function f).
        return inner


def astopwatch(
        f=None,
        message_template='Time taken: $time_ seconds',
        fmt='%.4g',
        logger=logger,
):
    # Using templates because safe_substitute is awesome.
    tmpl = Template(message_template)
    t0 = 0

    def pre_callback(sig, template_parameters):
        nonlocal t0
        t0 = time.perf_counter()

    def post_callback(sig, template_parameters):
        nonlocal t0
        dt = time.perf_counter() - t0
        msg = tmpl.safe_substitute(
            **template_parameters,
            time_=fmt % dt
        )
        logger.info(msg)

    return adecorator(
        f,
        pre_callback=pre_callback,
        post_callback=post_callback
    )
