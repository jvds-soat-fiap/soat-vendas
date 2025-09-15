from typing import TypeVar, Any, List
from dataclasses import dataclass
import pymongo
from pymongo import mongo_client
from pymongo.collection import ReturnDocument
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import json
from fastapi import status
from fastapi.encoders import jsonable_encoder
from decimal import Decimal
from bson.decimal128 import Decimal128
from src.util.logger_custom import Logger
from src.application.config.app_config import AppConfig
from src.application.exception.business_exception import BusinessException
from src.adapters.output.repository.database import Database
from dataclasses import asdict


# tipagem para model
T = TypeVar("T")

# tipagem para primary key
K = TypeVar("K")



config = AppConfig.from_json("./app/app-config.json")
db = None
try:
    __engine_client = mongo_client.MongoClient(host=config.database.db_url, connectTimeoutMS=20000, socketTimeoutMS=20000)
    db = __engine_client[config.database.db_name]
    VehicleTable = db.get_collection("vendas")
    Logger.info(method="database_mongodb", message=f"Configurado o database: {config.database.db_url}")    
except Exception as ex:
    Logger.error(method="database_mongodb", message=f"Error connection database to mongodb exception: {str(ex)}")


class DatabaseMongo(Database[T,K]):
    def __init__(self, modelType: T = None):
        self._modelType: str = self._getModelType(modelType)

    def insert(self, model: T) -> T:
        try:
            self._getModelType(model)
            session = db.get_collection(self._modelType)
#            model = session.insert_one(jsonable_encoder(model)); 
            model = session.insert_one(asdict(model)); 
            return model
        except DuplicateKeyError as ex:
            # {'index': 0, 'code': 11000, 'errmsg': 'E11000 duplicate key error collection: soat_order_db.product index: code_1 dup key: { code: "COCA350" }', 'keyPattern': {'code': 1}, 'keyValue': {'code': 'COCA350'}}
            keyValueError = ex.details['keyValue']
            raise BusinessException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Already exists {self._modelType.upper()} with value: {keyValueError}")
     
    def delete(self, id: K, modelType: T) -> bool:
        return super().delete(id, modelType)
    
    def update(self, model: T) -> T:
        try:
            # print(model.id)
            self._getModelType(model)
            session = db.get_collection(self._modelType)   
            filter = { '_id': f"{model._id}" }
            updateValues = { "$set": model.__dict__ }
            return session.update_one(filter, updateValues)
        except Exception as ex:
            raise ex
    
    def findById(self, id: K, modelType: T) -> T:
        # model = db_collection.find_one({"_id": ObjectId(id)})
        db_collection = db.get_collection(self._getModelType(modelType))
        result = db_collection.find_one({"_id": id})
        print(f"O valor do resultado e :{result}")
        # if (result is None):
        #     raise BusinessException(status_code=status.HTTP_409_CONFLICT,
        #                 detail=f"Search not found  to {id}")
        return result

    # https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/specify-query/
#    def findByFilter(self, modelType: T, filter: dict) -> T:
    def findByFilter(self, modelType: T, filter: dict):
        db_collection = db.get_collection(self._modelType)        
        resultCursor = db_collection.find(filter)
        return resultCursor

    def findByFilterOne(self, filter: dict) -> T:
        db_collection = db.get_collection(self._modelType)
        result = db_collection.find_one(filter=filter) 
        return result

    def findByAll(self, modelType: T) -> T:
        db_collection = db.get_collection(self._getModelType(modelType))
        return db_collection.find()

    def _getModelType(self, modelType: T) -> str:
        self._modelType = str(modelType.__name__ if isinstance(modelType,type) else modelType.__class__.__name__).lower()
        return self._modelType

    def _getSession(self):
        session_collection = db.get_collection(self._modelType)
        return session_collection
    
    #https://stackoverflow.com/questions/61456784/pymongo-cannot-encode-object-of-type-decimal-decimal
    def __convert_decimal(self,dict_item):
        # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
        # Embedded dictionaries and lists are called recursively.
        if dict_item is None:
            return None
        for k, v in list(dict_item.items()):
            if isinstance(v, dict):
                self.convert_decimal(v)
            elif isinstance(v, list):
                for l in v:
                    self.convert_decimal(l)
            elif isinstance(v, Decimal):
                dict_item[k] = Decimal(str(v))
            # elif isinstance(v, Decimal):
            #     dict_item[k] = Decimal128(str(v))
        return dict_item
