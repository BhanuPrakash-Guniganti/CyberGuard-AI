import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from backend.app.core.config import settings

logger = logging.getLogger("cyberguard.db")

# In-memory + file-persisted Document Store fallback
LOCAL_DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "cyberguard_db.json")

class LocalCollection:
    def __init__(self, name: str, parent_db):
        self.name = name
        self.parent = parent_db

    def _get_data(self) -> List[Dict[str, Any]]:
        return self.parent._storage.setdefault(self.name, [])

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for doc in self._get_data():
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return dict(doc)
        return None

    async def find(self, query: Optional[Dict[str, Any]] = None, sort: Optional[List] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = query or {}
        results = []
        for doc in self._get_data():
            match = True
            for k, v in query.items():
                if isinstance(v, dict):
                    if "$in" in v and doc.get(k) not in v["$in"]:
                        match = False
                        break
                    if "$gte" in v and doc.get(k, 0) < v["$gte"]:
                        match = False
                        break
                    if "$lte" in v and doc.get(k, 0) > v["$lte"]:
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                results.append(dict(doc))
        
        if sort:
            # Sort format: [("field", 1 or -1)]
            for field, order in reversed(sort):
                results.sort(key=lambda x: x.get(field, 0) or 0, reverse=(order == -1))

        if limit:
            results = results[:limit]

        return results

    async def insert_one(self, doc: Dict[str, Any]):
        doc_copy = dict(doc)
        if "_id" not in doc_copy:
            doc_copy["_id"] = f"{self.name}_{len(self._get_data()) + 1}"
        self._get_data().append(doc_copy)
        self.parent.save()
        return doc_copy

    async def insert_many(self, docs: List[Dict[str, Any]]):
        for doc in docs:
            await self.insert_one(doc)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        docs = self._get_data()
        for idx, doc in enumerate(docs):
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                if "$set" in update:
                    docs[idx].update(update["$set"])
                else:
                    docs[idx].update(update)
                self.parent.save()
                return True
        return False

    async def delete_many(self, query: Dict[str, Any]):
        docs = self._get_data()
        if not query:
            self.parent._storage[self.name] = []
            self.parent.save()
            return
        self.parent._storage[self.name] = [
            d for d in docs if not all(d.get(k) == v for k, v in query.items())
        ]
        self.parent.save()

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        docs = await self.find(query)
        return len(docs)

class DatabaseManager:
    def __init__(self):
        self._storage: Dict[str, List[Dict[str, Any]]] = {}
        self.is_connected_to_mongo = False
        self.client = None
        self.db = None
        self._load_local()

    def _load_local(self):
        os.makedirs(os.path.dirname(LOCAL_DB_FILE), exist_ok=True)
        if os.path.exists(LOCAL_DB_FILE):
            try:
                with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                    self._storage = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load local db file: {e}")
                self._storage = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(LOCAL_DB_FILE), exist_ok=True)
            with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(self._storage, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save local db: {e}")

    async def connect(self):
        try:
            import motor.motor_asyncio
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=1500
            )
            # Ping
            await self.client.admin.command('ping')
            self.db = self.client[settings.DB_NAME]
            self.is_connected_to_mongo = True
            logger.info(f"Connected successfully to MongoDB at {settings.MONGODB_URI}")
        except Exception as e:
            self.is_connected_to_mongo = False
            logger.info(f"MongoDB not available ({e}). Using local persistent document storage.")

    def get_collection(self, name: str):
        if self.is_connected_to_mongo and self.db is not None:
            # Wrap motor collection to maintain consistent interface
            return self.db[name]
        return LocalCollection(name, self)

db_manager = DatabaseManager()

def get_db():
    return db_manager
