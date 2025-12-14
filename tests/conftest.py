"""Configuración de pytest y fixtures compartidos."""

from unittest.mock import AsyncMock

import pytest

from ravexrpc import RPC_Client


@pytest.fixture
def mock_client():
    """Fixture que proporciona un cliente RPC mockeado."""
    client = RPC_Client()
    client._fetch = AsyncMock()
    return client


@pytest.fixture
def sample_token_accounts_response():
    """Fixture con respuesta de ejemplo para get_token_accounts."""
    return {
        "result": {
            "total": 2,
            "limit": 10,
            "cursor": None,
            "token_accounts": [
                {
                    "address": "TokenAccount1Address",
                    "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    "owner": "OwnerAddress",
                    "amount": 1000000,
                    "delegated_amount": 0,
                    "frozen": False,
                },
                {
                    "address": "TokenAccount2Address",
                    "mint": "So11111111111111111111111111111111111111112",
                    "owner": "OwnerAddress",
                    "amount": 5000000000,
                    "delegated_amount": 0,
                    "frozen": False,
                },
            ],
        }
    }


@pytest.fixture
def sample_transaction_response():
    """Fixture con respuesta de ejemplo para get_transaction."""
    return {
        "result": {
            "meta": {
                "postBalances": [1000000000, 2000000000, 3000000000],
                "preBalances": [1500000000, 1500000000, 3000000000],
            },
            "transaction": {
                "message": {
                    "accountKeys": [
                        "Account1Address",
                        "Account2Address",
                        "Account3Address",
                    ]
                }
            },
        }
    }


@pytest.fixture
def sample_rpc_error():
    """Fixture con respuesta de error RPC."""
    return {
        "error": {
            "code": -32602,
            "message": "Invalid params: invalid owner address",
        }
    }
