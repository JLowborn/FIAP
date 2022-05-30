""" Database Band Model """


from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder


class Band:
    def __init__(self, raw_data: dict):
        """
        Expects a dictionary to fill required fields
        """
        self._id: str = raw_data["_id"]
        self.nome: str = raw_data["nome"]
        self.banda: str = raw_data["banda"]
        self.ano: str = raw_data["ano"]
        self.categorias: List[str] = raw_data["categorias"]
        self.data_registro: datetime = raw_data["data_registro"]

    def json(self):
        """
        Returns parsed json data
        """
        return jsonable_encoder(self, exclude_none=True)


if __name__ == "__main__":

    # Testing
    band = Band(
        {
            "_id": "nODDmTpAf",
            "nome": "All Star",
            "banda": "Smash Mouth",
            "ano": "1999",
            "categorias": ["pop", "rock"],
            "data_registro": None,
        }
    )
    print(band.json())
