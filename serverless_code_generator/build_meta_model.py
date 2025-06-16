from dataclasses import dataclass
from typing import List
from .utils import MetaModel, Table, Column

@dataclass
class DataClassModel:
    tables: List[Table]

    def get_table(self, name: str) -> Table:
        for t in self.tables:
            if t.name == name:
                return t
        raise KeyError(name)


def build_meta_model(model: MetaModel) -> DataClassModel:
    return DataClassModel(model.tables)
