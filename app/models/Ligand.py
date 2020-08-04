from pydantic import BaseModel

class Ligand(BaseModel):

    id = ""
    name = ""
    external_code = ""
    biomol_code = ""
    structure_id = 0

