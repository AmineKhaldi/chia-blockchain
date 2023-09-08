from __future__ import annotations

import random
import string
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator, Union

from chia.util.db_wrapper import DBWrapper2


def gen_in_memory_db_uri(prefix: str) -> str:
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(8))
    return f"file:{prefix}{random_string}?mode=memory&cache=shared"


@asynccontextmanager
async def DBConnection(db_version: int, in_memory_db: bool = True) -> AsyncIterator[DBWrapper2]:
    if in_memory_db:
        directory = None
        db_path: Union[str, Path] = gen_in_memory_db_uri("db_cnx_")
    else:
        directory = tempfile.TemporaryDirectory()
        db_path = Path(directory.name).joinpath("db.sqlite")
    _db_wrapper = await DBWrapper2.create(database=db_path, uri=in_memory_db, reader_count=4, db_version=db_version)
    try:
        yield _db_wrapper
    finally:
        await _db_wrapper.close()
        if directory is not None:
            directory.cleanup()
