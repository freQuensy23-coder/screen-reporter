import pytest
from unittest.mock import patch, MagicMock
from models import User
from usecase import login, register_user
import peewee

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = 1
    user.secret_key = "test_secret_key"
    user.is_active = True
    return user

@patch('usecase.User')
def test_login_successful(mock_user_model, mock_user):
    # Setup
    mock_user_model.get_or_none.return_value = mock_user
    
    # Execute
    result, error = login(user_id=1, user_key="test_secret_key")
    
    # Assert
    assert result is True
    assert error is None
    mock_user_model.get_or_none.assert_called_once()

@patch('usecase.User')
def test_login_invalid_credentials(mock_user_model):
    # Setup
    mock_user_model.get_or_none.return_value = None
    
    # Execute
    result, error = login(user_id=1, user_key="wrong_key")
    
    # Assert
    assert result is False
    assert error == "Invalid credentials or user is inactive"

@patch('usecase.User')
def test_login_exception(mock_user_model):
    # Setup
    mock_user_model.get_or_none.side_effect = Exception("Database error")
    
    # Execute
    result, error = login(user_id=1, user_key="test_secret_key")
    
    # Assert
    assert result is False
    assert error == "Error during login"

@patch('usecase.User')
def test_register_user_successful(mock_user_model, mock_user):
    # Setup
    mock_user_model.create.return_value = mock_user
    
    # Execute
    user, error = register_user()
    
    # Assert
    assert user is not None
    assert error is None
    assert mock_user_model.create.called
    create_args = mock_user_model.create.call_args[1]
    assert 'secret_key' in create_args
    assert create_args['is_active'] is True

@patch('usecase.User')
def test_register_user_integrity_error(mock_user_model):
    # Setup
    mock_user_model.create.side_effect = peewee.IntegrityError()
    
    # Execute
    user, error = register_user()
    
    # Assert
    assert user is None
    assert error == "Failed to create user due to database constraint"

@patch('usecase.User')
def test_register_user_unexpected_error(mock_user_model):
    # Setup
    mock_user_model.create.side_effect = Exception("Unexpected error")
    
    # Execute
    user, error = register_user()
    
    # Assert
    assert user is None
    assert error == "Unexpected error during user registration"

