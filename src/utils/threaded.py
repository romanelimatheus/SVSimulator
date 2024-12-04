from collections.abc import Callable
from functools import wraps as functools_wraps
from threading import Thread
from typing import Any


def threaded(fn: Callable[..., Any]) -> Callable[..., Thread]:
    @functools_wraps(fn)
    def _threaded(*args: Any, **kw: Any) -> Thread:
        t = Thread(target=fn, args=args, kwargs=kw, daemon=True)
        t.start()
        return t

    return _threaded
