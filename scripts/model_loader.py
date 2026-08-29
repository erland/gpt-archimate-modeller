from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from assemble_project import assemble
from model_index import load_valid_index

def load_model(project_root,use_index=True):
    root=Path(project_root)
    if use_index:
        logical,status=load_valid_index(root)
        if logical is not None:
            return logical,[],{"source":"index","index_status":status}
    logical,errors=assemble(root)
    return logical,errors,{"source":"yaml","index_status":"missing_or_stale" if use_index else "disabled"}
