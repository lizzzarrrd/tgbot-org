import pytest
from unittest.mock import AsyncMock, MagicMock
from tg_bot.use_cases.bd_interactor import BdInteractor
from tg_bot.domain import User


@pytest.mark.asyncio
async def test_get_by_telegram_id_found():
    mock_session = AsyncMock()
    mock_user = User(telegram_id=123456)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = mock_result
    
    interactor = BdInteractor(mock_session)
    user = await interactor.get_by_telegram_id(123456)
    
    assert user == mock_user
    assert user.telegram_id == 123456
    mock_session.execute.assert_called_once()



@pytest.mark.asyncio
async def test_create_user():
    mock_session = AsyncMock()
    
    interactor = BdInteractor(mock_session)
    user = await interactor.create(123456)
    
    assert user.telegram_id == 123456
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_get_or_create_existing():
    mock_session = AsyncMock()
    existing_user = User(telegram_id=123456)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_user
    mock_session.execute.return_value = mock_result
    
    interactor = BdInteractor(mock_session)
    user = await interactor.get_or_create(123456)
    
    assert user == existing_user
    assert user.telegram_id == 123456
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()

