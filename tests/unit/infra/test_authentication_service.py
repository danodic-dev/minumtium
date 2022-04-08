import pytest

from minumtium.infra.authentication import AuthenticationService, AuthenticationException


def test_validate_token(auth_service: AuthenticationService):
    auth_service.validate_token('valid')


def test_validate_invalid_token(auth_service: AuthenticationService):
    with pytest.raises(AuthenticationException) as e:
        auth_service.validate_token('invalid')
        assert e.value.args[0] == "Invalid token."


def test_authenticate(auth_service: AuthenticationService):
    token = auth_service.authenticate('valid', 'valid')
    assert token == 'valid'


def test_authenticate_invalid_username(auth_service: AuthenticationService):
    with pytest.raises(AuthenticationException) as e:
        auth_service.authenticate('invalid', 'valid')
        assert e.type is AuthenticationException
        assert e.value.args[0] == "Invalid username and/or password."


def test_authenticate_invalid_password(auth_service: AuthenticationService):
    with pytest.raises(AuthenticationException) as e:
        auth_service.authenticate('valid', 'invalid')
        assert e.type is AuthenticationException
        assert e.value.args[0] == "Invalid username and/or password."
