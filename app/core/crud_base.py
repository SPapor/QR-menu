from typing import ClassVar, Sequence

from sqlalchemy import Table, delete, func, insert, literal, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CrudBase[ID, DTO]:
    table: ClassVar[Table]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_: ID) -> DTO | None:
        res = await self.session.execute(select(self.table).where(self.table.c.id == literal(id_)))
        return res.mappings().one_or_none()

    async def create(self, obj: DTO) -> ID:
        res = await self.session.execute(insert(self.table).values(**obj))
        pk = res.inserted_primary_key
        return pk[0] if len(pk) == 1 else pk

    async def create_and_get(self, obj: DTO) -> DTO:
        res = await self.session.execute(insert(self.table).values(**obj).returning(self.table))
        return res.mappings().one_or_none()

    async def create_many(self, objs: Sequence[DTO]) -> list[ID]:
        objs = list(objs)
        if len(objs) == 0:
            return []
        res = await self.session.execute(insert(self.table).values(objs).returning(self.table.c.id))
        return [row[0] for row in res.all()]

    async def create_and_get_many(self, objs: Sequence[DTO]) -> Sequence[DTO]:
        objs = list(objs)
        if len(objs) == 0:
            return []
        res = await self.session.execute(insert(self.table).values(objs).returning(self.table))
        return res.mappings().all()

    async def update(self, values: DTO) -> None:
        id_ = values.pop("id")
        if not values:
            return
        await self.session.execute(
            update(self.table).where(self.table.c.id == literal(id_)).values(values).returning(self.table)
        )

    async def update_many(self, objs: Sequence[DTO]) -> None:
        for obj in objs:
            id_ = obj.pop("id")
            await self.session.execute(
                update(self.table).where(self.table.c.id == literal(id_)).values(obj).returning(self.table)
            )

    async def get_many_by_ids(self, ids: Sequence[ID]) -> Sequence[DTO]:
        for id_ in ids:
            res = await self.session.execute(select(self.table).where(self.table.c.id == literal(id_)))
            return res.mappings().all()

    async def delete(self, id_: ID) -> None:
        await self.session.execute(delete(self.table).where(self.table.c.id == literal(id_)))

    async def delete_many(self, ids: Sequence[ID]) -> None:
        await self.session.execute(delete(self.table).where(self.table.c.id.in_(ids)))

    async def count(self) -> int:
        res = await self.session.execute(select(func.count()).select_from(self.table))
        return res.scalar()

    async def get_all(self) -> Sequence[DTO]:
        res = await self.session.execute(select(self.table))
        return res.mappings().all()
