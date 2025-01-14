from collections.abc import Iterable, Mapping
from typing import Generic, cast

from tinydb import Storage
from tinydb.queries import QueryLike
from tinydb.table import Document, Table

from lib.orm.schemas import SchemaType
from lib.utils import hsash, logger


class FADocument(dict):  # noqa: FURB189
    """
    A document stored in the database.

    This class provides a way to access both a document's content and
    its ID using ``doc.doc_id``.
    """

    def __init__(self, value: Mapping, doc_id: str) -> None:
        super().__init__(value)
        self.doc_id = doc_id


class FATable(Table, Generic[SchemaType]):
    """TinyDB wrapper enforcing schema on insert and returning typed records."""

    LOG_PREFIX = "[FAORM] -"

    schema: type[SchemaType]

    document_class = FADocument
    document_id_class = str

    def __init__(self, storage: Storage, name: str, schema: type[SchemaType]) -> None:
        self.schema = schema

        super().__init__(storage=storage, name=name)

    def remove(
        self,
        cond: QueryLike | None = None,
        doc_ids: list | None = None,
    ) -> None:
        """
        Remove documents from the table.

        Parameters
        ----------
        cond : Optional[QueryLike]
            The condition to match.
        doc_ids : Optional[List]
            The list of document IDs to match.

        """
        super().remove(cond, doc_ids)

    @staticmethod
    def generate_hash(entry: SchemaType) -> str:
        """
        Generate a hash for the entry.

        Parameters
        ----------
        entry : SchemaType
            The entry to hash.

        Returns
        -------
        str
            The generated hash.

        """
        return hsash.hsh(entry.model_dump(exclude={"uid"}))

    def get(
        self,
        cond: QueryLike | None = None,
        doc_id: str | None = None,
        doc_ids: list | None = None,
    ) -> Document | list[Document] | None:
        """
        Get a document or documents from the table.

        Parameters
        ----------
        cond : Optional[QueryLike]
            The condition to match.
        doc_id : Optional[str]
            The document ID to match.
        doc_ids : Optional[List]
            The list of document IDs to match.

        Returns
        -------
        Optional[Union[Document, List[Document]]]
            The matching document or documents.

        """
        return super().get(cond, doc_id, doc_ids)  # type: ignore  # noqa: PGH003

    def find_by_uid(self, uid: str) -> SchemaType | None:
        """Find an entry by UID."""
        doc = self.get(doc_id=uid)

        if doc is None:
            logger.warning(f"{self.LOG_PREFIX} Document with UID {uid} not found")
            return None

        if isinstance(doc, list):
            return self.schema(**doc[0])

        return self.schema(**doc)

    def insert(self, data: SchemaType, uid: str) -> SchemaType:
        """
        Create a new entry.

        Parameters
        ----------
        data : SchemaType
            The data to insert.
        uid : str, optional
            The UID to use.

        Returns
        -------
        SchemaType
            The inserted data.

        """
        super().insert(FADocument(data.model_dump(), doc_id=uid))
        return data

    def update(
        self,
        data: SchemaType,
        cond: QueryLike | None = None,
        doc_ids: Iterable[int] | None = None,
    ) -> SchemaType:
        """
        Update an entry.

        Parameters
        ----------
        data : SchemaType
            The data to update.
        cond : QueryLike, optional
            The condition to update.
        doc_ids : Iterable[int], optional
            The document IDs to update.

        Returns
        -------
        SchemaType
            The updated data.

        """
        data.uid = data.uid or self.generate_hash(data)
        super().update(data.model_dump(), cond, doc_ids)
        return data

    def all(self) -> list[SchemaType]:
        """
        Return all entries.

        Returns
        -------
        list[SchemaType]
            All entries in the table.

        """
        return cast("list[SchemaType]", [self.schema(**doc) for doc in super().all()])

    def search(self, cond: QueryLike) -> list[SchemaType]:
        """
        Search for all documents matching a condition.

        Parameters
        ----------
        cond : QueryLike
            The condition to search for.

        Returns
        -------
        list[SchemaType]
            The matching documents.

        """
        return cast(
            "list[SchemaType]",
            [self.schema(**doc) for doc in super().search(cond)],
        )
