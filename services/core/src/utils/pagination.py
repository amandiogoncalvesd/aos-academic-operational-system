import math
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.common import PaginatedResponse, PaginationParams


async def paginate(db: AsyncSession, query: Select, params: PaginationParams) -> PaginatedResponse[Any]:
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()
    rows = (await db.execute(query.offset(params.offset).limit(params.page_size))).scalars().all()
    return PaginatedResponse(
        items=list(rows), total=total, page=params.page, page_size=params.page_size,
        pages=max(1, math.ceil(total / params.page_size)),
    )
