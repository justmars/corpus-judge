from pathlib import Path

import pytest
import yaml
from sqlite_utils import Database

temppath = "test.db"


@pytest.fixture
def justice_records(shared_datadir) -> list[dict]:
    f: Path = shared_datadir / "sc.yaml"
    return yaml.safe_load(f.read_bytes())


@pytest.fixture
def session(justice_records, shared_datadir):
    p = shared_datadir / temppath
    db = Database(p)
    db["sc_tbl_justices"].insert_all(justice_records)  # type: ignore
    yield db
    db.close()  # close the connection
    p.unlink()
