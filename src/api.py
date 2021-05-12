from typing import List

import aiofiles
import ormar
from fastapi import APIRouter, BackgroundTasks, File, UploadFile, HTTPException, status

from src.config import settings
from src.models import Calculation
from src.services import get_lists_for_comparison
from src.utils import create_file_path, equalize_lists

app_router = APIRouter(
    prefix='/calculations',
)


@app_router.get('/', response_model=List[Calculation])
async def get_items():
    items = await Calculation.objects.all()
    return items


@app_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_item(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    if file.content_type not in settings.allow_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Mime type not allowed for file upload.'
        )

    file_path = await create_file_path(file.filename)
    await save_file(file_path, file)
    calculation = await Calculation.objects.create(file=file_path)
    background_tasks.add_task(update_calculation, file.content_type, calculation.id)
    return {'calculation_id': calculation.id}


@app_router.get('/{item_id}', response_model=Calculation)
async def get_item(item_id: int):
    try:
        return await Calculation.objects.get(id=item_id)
    except ormar.NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found.'
        )


async def save_file(file_path: str, file: UploadFile):
    async with aiofiles.open(file_path, 'wb') as buffer:
        data = await file.read()
        await buffer.write(data)


async def update_calculation(content_type: str, calculation_id: int) -> None:
    calculation = await Calculation.objects.get(id=calculation_id)
    file_path = calculation.file
    await calculation.set_processed_status()
    lists_for_calculation = get_lists_for_comparison(content_type, file_path)
    num, action = equalize_lists(*lists_for_calculation)
    await calculation.set_finished_status(value=num, action=action)
