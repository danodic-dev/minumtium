from typing import Dict

import pytest

from minumtium.infra.database import DataNotFoundException
from minumtium.modules.idm import User, UserRepository, NoUserFoundException


def test_get_by_id(repo: UserRepository):
    user = repo.get_by_id('0')
    assert type(user) is User
    assert user.username == 'valid'
    assert user.encrypted_password == 'abc123'


def test_get_by_id_invalid_id(repo: UserRepository):
    with pytest.raises(NoUserFoundException) as e:
        repo.get_by_id('-1')
        assert e.type is NoUserFoundException
        assert e.value.args[0] == "Invalid username: invalid"


def test_get_by_username(repo: UserRepository):
    user = repo.get_by_username(username='valid')
    assert type(user) is User
    assert user.username == 'valid'
    assert user.encrypted_password == 'abc123'


def test_get_by_username_invalid_username(repo: UserRepository):
    with pytest.raises(NoUserFoundException) as e:
        repo.get_by_username(username='invalid')
        assert e.type is NoUserFoundException
        assert e.value.args[0] == "Invalid username: invalid"


def test_save(repo: UserRepository):
    user_id = repo.save(User(username='valid', encrypted_password='abc123'))
    assert user_id == '0'


@pytest.fixture()
def repo() -> UserRepository:
    class MockAdapter:
        def find_by_id(self, id: str):
            if id == '0':
                return {'id': '0',
                        'username': 'valid',
                        'encrypted_password': 'abc123'}
            return NoUserFoundException(id)

        def find_by_criteria(self, criteria: Dict):
            def apply_filter(entry: Dict):
                for key, value in criteria.items():
                    if entry[key] != value:
                        return False
                return True

            result = list(filter(apply_filter, self.all()))
            if len(result) > 0:
                return result
            raise DataNotFoundException(criteria)

        def insert(self, data: Dict):
            return '0'

        def all(self, limit: int = None, skip: int = None):
            return [{'id': '0',
                     'username': 'valid',
                     'encrypted_password': 'abc123'}]

    adapter = MockAdapter()
    return UserRepository(adapter)
