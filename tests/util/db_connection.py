from __future__ import annotations

import random
import string
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from chia.util.db_wrapper import DBWrapper2


def gen_in_memory_db_uri() -> str:
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(8))
    return f"file:{random_string}?mode=memory&cache=shared"


@asynccontextmanager
async def DBConnection(db_version: int) -> AsyncIterator[DBWrapper2]:
    db_uri = gen_in_memory_db_uri()
    _db_wrapper = await DBWrapper2.create(database=db_uri, uri=True, reader_count=4, db_version=db_version)
    try:
        yield _db_wrapper
    finally:
        await _db_wrapper.close()


@asynccontextmanager
async def PathDBConnection(db_version: int) -> AsyncIterator[DBWrapper2]:
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory).joinpath("db.sqlite")
        _db_wrapper = await DBWrapper2.create(database=db_path, reader_count=4, db_version=db_version)
        try:
            yield _db_wrapper
        finally:
            await _db_wrapper.close()
