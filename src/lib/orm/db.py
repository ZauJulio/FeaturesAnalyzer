import os
from pathlib import Path

from tinydb import TinyDB

from lib.orm.schemas import SchemasKeys, SchemaType
from lib.orm.table import FATable


class MissingDBEntryError(Exception):
    """Raised when a database entry is missing."""


class TypedTinyDB(TinyDB):
    """TinyDB wrapper enforcing schema and typed records."""

    db: TinyDB
    base_path: Path

    _tables: dict[str, FATable]
    table_class: type[FATable]
    document_id_class: str

    def __init__(self, path: str | None = None) -> None:
        self.base_path = Path(path or os.getenv("DB_PATH", "../"))

        super().__init__(self.base_path)

    def table(
        self,
        name: SchemasKeys,
        schema: type[SchemaType],
    ) -> FATable[SchemaType]:
        """
        Return a typed table instance.

        Parameters
        ----------
        name : str
            The name of the table.
        schema : type[SchemaType]
            The schema class to enforce.
        kwargs : dict[str, str]
            Additional arguments to pass to the table.

        Returns
        -------
        FATable
            The table instance.

        """
        if name in self._tables:
            return self._tables[name]

        self._tables[name] = FATable(
            name=name,
            storage=self.storage,
            schema=schema,
        )

        return self._tables[name]


from lib.orm.schemas import FAModelSchema, FAPreProcessorSchema

db = TypedTinyDB()

ModelTable = db.table("FAModel", FAModelSchema)
PreProcessorTable = db.table("FAPreProcessor", FAPreProcessorSchema)
