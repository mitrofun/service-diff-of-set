import pytest

from src.utils import equalize_lists, create_file_path


@pytest.mark.parametrize('left_list, right_list, expected', 
    [
        ([1, 2], [1, 2, 3], (3, 'added')),
        ([1, 2, 3, 4], [1, 2, 4], (3, 'removed')),
        ([1, 2, 3, 4, 5], [1, 3, 4, 5, 2], None),
        ([], [], None),
        ([], [1], (1, 'added')),
        ([1], [], (1, 'removed')),
    ]
)
def test_equalize_lists(left_list, right_list, expected):
    assert equalize_lists(left_list, right_list) == expected


@pytest.mark.asyncio
async def test_create_file_path():
    file = await create_file_path('test')
    assert file == 'tmp/test'
