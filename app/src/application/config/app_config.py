import json
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    db_url: str
    db_name: str


@dataclass
class AppConfig:
    database: DatabaseConfig

    @classmethod
    def from_json(cls, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(
            database=DatabaseConfig(**data['database']),
        )