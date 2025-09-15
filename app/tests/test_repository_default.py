import unittest
from unittest.mock import MagicMock, patch
from typing import Any
from src.application.exception.business_exception import BusinessException
from src.adapters.output.repository.repository_default import RepositoryDefault

# Modelo fictício para testes
class DummyModel:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

# Subclasse concreta para testes
class TestRepository(RepositoryDefault):
    def parseToModel(self, dict: dict) -> DummyModel:
        return DummyModel(**dict)

class RepositoryDefaultTestCase(unittest.TestCase):
    def setUp(self):
        self.model_instance = DummyModel(id=1, name="Test")
        self.repo = TestRepository(modelType=DummyModel)
        self.repo.db = MagicMock()

    def test_save(self):
        self.repo.db.insert = MagicMock()
        result = self.repo.save(self.model_instance)
        self.repo.db.insert.assert_called_once_with(self.model_instance)
        self.assertEqual(result, self.model_instance)

    def test_update(self):
        self.repo.db.update = MagicMock(return_value=self.model_instance)
        result = self.repo.update(self.model_instance)
        self.repo.db.update.assert_called_once_with(self.model_instance)
        self.assertEqual(result, self.model_instance)

    def test_findById_success(self):
        self.repo.db.findById = MagicMock(return_value={"id": 1, "name": "Test"})
        result = self.repo.findById(1)
        self.repo.db.findById.assert_called_once_with(1, DummyModel)
        self.assertIsInstance(result, DummyModel)

    def test_findById_not_found(self):
        self.repo.db.findById = MagicMock(side_effect=Exception("Not found"))
        with self.assertRaises(BusinessException):
            self.repo.findById(999)

    def test_findByFilter(self):
        self.repo.db.findByFilter = MagicMock(return_value=[self.model_instance])
        result = self.repo.findByFilter({"name": "Test"})
        self.repo.db.findByFilter.assert_called_once()
        self.assertEqual(result, [self.model_instance])

    def test_findByFilterOne(self):
        self.repo.db.findByFilterOne = MagicMock(return_value={"id": 1, "name": "Test"})
        result = self.repo.findByFilterOne({"name": "Test"})
        self.repo.db.findByFilterOne.assert_called_once()
        self.assertIsInstance(result, DummyModel)

if __name__ == "__main__":
    unittest.main()
