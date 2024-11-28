from .connection import DBConnectionHandler
import pytest

@pytest.mark.skip(reason='Sensive test')
def test_create_database_engine():
    db_connetion_handle = DBConnectionHandler()
    engine = db_connetion_handle.get_engine()
    
    assert engine is not None