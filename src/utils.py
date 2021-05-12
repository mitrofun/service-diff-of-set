import os
import uuid

from typing import Tuple, Union, Optional
from pathlib import Path, _ignore_error as pathlib_ignore_error  # type: ignore  # noqa

import aiofiles.os

from .config import settings


def equalize_lists(left_items: list[Union[int, None]],
                   right_items: list[Union[int, None]]) -> Tuple[Optional[int], Optional[str]]:
    """
    Calculate needed operation
    return: Number and action: 'removed' or 'added'. or None, None
    """
    if set(left_items) == set(right_items):
        return None, None
    difference: set = set(left_items) ^ set(right_items)
    num = list(difference)[0]
    action = 'removed' if num in left_items else 'added'
    return num, action


async def create_file_path(filename: str) -> str:
    file_path = f'{settings.media_dir}/{filename}'
    if await path_exists(file_path):
        name, ext = os.path.splitext(filename)
        file_path = f'{settings.media_dir}/{name}_{str(uuid.uuid4())[:8]}{ext}'
    return file_path


async def path_exists(path: Union[Path, str]) -> bool:
    try:
        await aiofiles.os.stat(str(path))
    except OSError as e:
        if not pathlib_ignore_error(e):
            raise
        return False
    except ValueError:
        return False
    return True
