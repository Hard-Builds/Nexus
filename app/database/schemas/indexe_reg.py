from pymongo import ASCENDING, IndexModel

from app.enums.db_collections import DBCollections

db_index_registry = {
    DBCollections.USER_MST.value: [
        IndexModel(
            [('username', ASCENDING)],
            unique=True,
            name='username_index'
        )
    ],
    DBCollections.CREDENTIAL_MST.value: []
}
