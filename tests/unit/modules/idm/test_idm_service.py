from typing import Dict

import pytest

from minumtium.infra.authentication import AuthenticationAdapter, AuthenticationException
from minumtium.modules.idm import IdmService, UserRepository, InvalidUsernameOrPasswordException, EmptyUsernameException, \
    InvalidPasswordException


def test_is_valid_token(idm_service: IdmService):
    assert idm_service.is_valid_token(token='valid')


def test_is_valid_token_negative(idm_service: IdmService):
    assert not idm_service.is_valid_token(token='invalid')


def test_authenticate(idm_service: IdmService):
    token = idm_service.authenticate(username='valid', password='valid')
    assert token == 'abc123'


@pytest.mark.parametrize('username, password', [('valid', 'invalid'),
                                                ('invalid', 'valid')])
def test_authenticate_negative(username: str, password: str, idm_service: IdmService):
    with pytest.raises(InvalidUsernameOrPasswordException) as e:
        idm_service.authenticate(username=username, password=password)
        assert e.type is InvalidUsernameOrPasswordException
        assert e.value.args[0] == "Invalid username and/or password."


def test_put_user(idm_service: IdmService):
    assert not idm_service.put_user('validusername', 'valid')


def test_put_user_empty_username(idm_service: IdmService):
    with pytest.raises(EmptyUsernameException):
        idm_service.put_user('', 'valid')


def test_put_user_update(idm_service: IdmService):
    assert idm_service.put_user('valid', 'valid')


def test_put_user_invalid_password(idm_service: IdmService):
    with pytest.raises(InvalidPasswordException):
        idm_service.put_user('valid', 'invalid')


@pytest.fixture()
def idm_service(users_database_adapter) -> IdmService:
    class MockAuthAdapter(AuthenticationAdapter):
        def is_valid_password(self, password: str) -> bool:
            return password == 'valid'

        def get_password_criteria(self):
            pass

        def initialize(self, config: Dict, user_repo: UserRepository):
            pass

        def encrypt_password(self, password: str) -> str:
            return 'encrypted'

        def validate_token(self, token: str) -> bool:
            if token == 'valid':
                return True
            return False

        def authenticate(self, username: str, password: str) -> str:
            if username == 'valid' and password == 'valid':
                return 'abc123'
            raise AuthenticationException('Invalid username and/or password.')

    return IdmService(MockAuthAdapter(), UserRepository(users_database_adapter))
