import logging, os
from app.core.config import settings
from Bio.PDB.PDBParser import PDBParser

logger = logging.getLogger(__name__)
print("Hello")
str_id = '2po6'
parser = PDBParser()
structure = parser.get_structure(id=str_id, file=os.path.join(settings.PROJECT_PATH, 'saves', str_id + '.pdb'))
logger.info(structure)
exit()