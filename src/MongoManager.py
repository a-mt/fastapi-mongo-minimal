from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.database import Database

class MongoManager:
    def __init__(self, uri: str, tls: bool, db_name: str, coll_name: str):
        self.__client = MongoClient(
            uri,
            server_api=ServerApi('1') if tls else None,
            tls=tls,
            connectTimeoutMS=1000,
            socketTimeoutMS=1000,
            serverSelectionTimeoutMS=1000,
        )
        try:
            ping = self.__client.admin.command({'ping': 1})
            print(f"Pinged your deployment: {ping}. You successfully connected to MongoDB!")

        except Exception as e:
            raise Exception("Unable to connect to MongoDB due to the following error: ", e)

        self.__client.server_info()
        self.__db: Database = self.__client[db_name]
        self.__collection: Collection = self.__db[coll_name]

    # Getters and setters

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, db_name: str):
        self.__db = self.__client[db_name]
        # réaffectation obligatoire de la collection car changement de database
        self.collection = self.__collection.name # .name car collection est un objet

    @property
    def collection(self):
        return self.__collection

    @collection.setter
    def collection(self, coll_name: str):
        self.__collection = self.db[coll_name]

    # CRUD operations

    def create_one_document(self, document: dict):
        try:
            insert_result = self.collection.insert_one(document)
            return {"acknowledged": insert_result.acknowledged, "insertedId": insert_result.inserted_id}
        except Exception as e:
            raise Exception("Unable to insert the document due to the following error: ", e)

    def create_many_documents(self, documents: list[dict]):
        try:
            insert_result = self.collection.insert_many(documents)
            return {"acknowledged": insert_result.acknowledged, "insertedIds": insert_result.inserted_ids}
        except Exception as e:
            raise Exception("Unable to insert the documents due to the following error: ", e)

    def read_one_document(self, query: dict):
        try:
            document = self.collection.find_one(query)
            return document
        except Exception as e:
            raise Exception("Unable to read the document due to the following error: ", e)

    def read_many_documents(self, query: dict):
        try:
            documents = self.collection.find(query)
            return list(documents)
        except Exception as e:
            raise Exception("Unable to read the documents due to the following error: ", e)

    def update_one_document(self, query: dict, new_values: dict):
        try:
            update_result = self.collection.update_one(query, new_values)
            return {
                "acknowledged": update_result.acknowledged,
                "insertedId": update_result.upserted_id,
                "matchedCount": update_result.matched_count,
                "modifiedCount": update_result.modified_count,
            }
        except Exception as e:
            raise Exception("Unable to update the document due to the following error: ", e)

    def update_many_documents(self, query: dict, new_values: dict):
        try:
            update_result = self.collection.update_many(query, new_values)
            return {
                "acknowledged": update_result.acknowledged,
                "insertedId": update_result.upserted_id,
                "matchedCount": update_result.matched_count,
                "modifiedCount": update_result.modified_count,
            }
        except Exception as e:
            raise Exception("Unable to update the documents due to the following error: ", e)

    def delete_one_document(self, query: dict):
        try:
            delete_result = self.collection.delete_one(query)
            return {"acknowledged": delete_result.acknowledged, "deletedCount": delete_result.deleted_count}
        except Exception as e:
            raise Exception("Unable to delete the document due to the following error: ", e)

    def delete_many_documents(self, query: dict):
        try:
            delete_result = self.collection.delete_many(query)
            return {"acknowledged": delete_result.acknowledged, "deletedCount": delete_result.deleted_count}
        except Exception as e:
            raise Exception("Unable to delete the documents due to the following error: ", e)

    # Database operations

    def list_databases(self):
        try:
            databases = self.__client.list_database_names()
            return databases
        except Exception as e:
            raise Exception("Unable to list the databases due to the following error: ", e)

    def list_collections(self):
        try:
            collections = self.db.list_collection_names()
            return collections
        except Exception as e:
            raise Exception("Unable to list the collections due to the following error: ", e)

    def drop_database(self, db_name: str):
        try:
            self.__client.drop_database(db_name)
            return True
        except Exception as e:
            raise Exception("Unable to drop the database due to the following error: ", e)

    def close_connection(self):
        self.__client.close()
        print("Connection closed.")
