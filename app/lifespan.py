import contextlib
from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import AbstractAsyncContextManager
from fastapi import FastAPI


class Lifespan:
    def __init__(
        self,
        lifespans: Sequence[Callable[[FastAPI], AbstractAsyncContextManager[None]]],
    ) -> None:
        self.lifespans = lifespans

    def __call__(self, app: FastAPI) -> AbstractAsyncContextManager[None]:
        self.app = app
        return self._manager(app, lifespans=self.lifespans)

    @contextlib.asynccontextmanager
    async def _manager(
            self,
            app: FastAPI,
            lifespans: Sequence[Callable[[FastAPI], AbstractAsyncContextManager[None]]],
    ) -> AsyncIterator[None]:
        exit_stack = contextlib.AsyncExitStack()
        async with exit_stack:
            for lifespan in lifespans:
                await exit_stack.enter_async_context(lifespan(app))
            yield
