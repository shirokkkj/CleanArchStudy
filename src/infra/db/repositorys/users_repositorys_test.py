from .users_repository import UsersRepository
from src.infra.db.settings.connection import DBConnectionHandler
from sqlalchemy import text
import pytest

db_connection_handle = DBConnectionHandler()
connection = db_connection_handle.get_engine().connect()

@pytest.mark.skip(reason='Sensive test')
def test_insert_user():
    mocked_first_name = 'first'
    mocked_last_name = 'last'
    mocked_age = 34
    
    users_repository = UsersRepository()
    users_repository.insert_user(
        mocked_first_name,
        mocked_last_name,
        mocked_age
    )
    
    SQL = '''
    
    SELECT * FROM users
    WHERE first_name = '{}'
    AND last_name = '{}'
    AND age = {}
    
    '''.format(mocked_first_name, mocked_last_name, mocked_age)
    
    response = connection.execute(text(SQL))
    registry = response.fetchall()[0]
    
    assert registry.first_name == mocked_first_name
    assert registry.last_name == mocked_last_name
    assert registry.age == mocked_age

    connection.execute(text(f'''
    DELETE FROM users WHERE id = {registry.id}
'''))

@pytest.mark.skip(reason='Sensive test')
def test_select_user():
    first_name = 'first'
    last_name = 'last'
    age = 34

    sql = '''
    INSERT INTO users (first_name, last_name, age) VALUES ('{}', '{}', {})
    '''.format(first_name, last_name, age)
    
    connection.execute(text(sql))
    connection.commit()
    
    users_repository = UsersRepository()
    
    response = users_repository.select_user(first_name)
    
    assert response[0].first_name == first_name
    assert response[0].last_name == last_name
    assert response[0].age == age
    
    connection.execute(text(f'''
    DELETE FROM users WHERE id = {response[0].id}
'''))
