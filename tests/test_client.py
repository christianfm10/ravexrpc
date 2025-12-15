"""Tests para el módulo client."""

import pytest

from ravexrpc import RPC_Client
from ravexrpc.exceptions import RPCException


class TestRPCClient:
    """Tests para la clase RPC_Client."""

    def test_client_initialization_default(self):
        """Test de inicialización con valores por defecto."""
        client = RPC_Client()
        assert client.BASE_URL == "https://api.mainnet-beta.solana.com"

    def test_client_initialization_custom(self):
        """Test de inicialización con URL personalizada."""
        custom_url = "https://api.devnet.solana.com"
        client = RPC_Client(base_url=custom_url)
        # Verificar que se inicializó correctamente
        assert client is not None


class TestGetTokenAccounts:
    """Tests para el método get_token_accounts."""

    @pytest.mark.asyncio
    async def test_get_token_accounts_success(
        self, mock_client, sample_token_accounts_response
    ):
        """Test exitoso de get_token_accounts."""
        mock_client._fetch.return_value = sample_token_accounts_response

        result = await mock_client.get_token_accounts(
            owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"
        )

        assert result.total == 2
        assert result.limit == 10
        assert len(result.token_accounts) == 2
        assert result.token_accounts[0].amount == 1000000

    @pytest.mark.asyncio
    async def test_get_token_accounts_with_mint(
        self, mock_client, sample_token_accounts_response
    ):
        """Test de get_token_accounts con filtro de mint."""
        mock_client._fetch.return_value = sample_token_accounts_response

        result = await mock_client.get_token_accounts(
            owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
            mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        )

        assert result.total == 2
        # Verificar que se llamó con los parámetros correctos
        call_args = mock_client._fetch.call_args
        assert "mint" in call_args[1]["payload"]["params"]

    @pytest.mark.asyncio
    async def test_get_token_accounts_with_options(
        self, mock_client, sample_token_accounts_response
    ):
        """Test de get_token_accounts con opciones adicionales."""
        mock_client._fetch.return_value = sample_token_accounts_response

        result = await mock_client.get_token_accounts(
            owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
            show_zero_balance=True,
            limit=50,
        )

        assert result.total == 2
        # Verificar que se pasaron las opciones correctamente
        call_args = mock_client._fetch.call_args
        payload = call_args[1]["payload"]
        assert payload["params"]["limit"] == 50
        assert payload["params"]["options"]["showZeroBalance"] is True

    @pytest.mark.asyncio
    async def test_get_token_accounts_invalid_owner(self, mock_client):
        """Test con owner inválido."""
        with pytest.raises(ValueError, match="cadena válida"):
            await mock_client.get_token_accounts(owner="")

        with pytest.raises(ValueError, match="cadena válida"):
            await mock_client.get_token_accounts(owner=None)

    @pytest.mark.asyncio
    async def test_get_token_accounts_rpc_error(self, mock_client, sample_rpc_error):
        """Test con error RPC."""
        mock_client._fetch.return_value = sample_rpc_error

        with pytest.raises(RPCException, match="Error RPC"):
            await mock_client.get_token_accounts(
                owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"
            )


class TestGetTransaction:
    """Tests para el método get_transaction."""

    @pytest.mark.asyncio
    async def test_get_transaction_success(
        self, mock_client, sample_transaction_response
    ):
        """Test exitoso de get_transaction."""
        mock_client._fetch.return_value = sample_transaction_response

        result = await mock_client.get_transaction(
            signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9"
        )

        assert result.meta is not None
        assert len(result.meta.pre_balances) == 3
        assert len(result.meta.post_balances) == 3
        assert len(result.meta.delta_balances) == 3

    @pytest.mark.asyncio
    async def test_get_transaction_with_accounts(
        self, mock_client, sample_transaction_response
    ):
        """Test de get_transaction con cálculo de montos."""
        mock_client._fetch.return_value = sample_transaction_response

        result = await mock_client.get_transaction(
            signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9",
            from_pk="Account1Address",
            to_pk="Account2Address",
        )

        # Account1: 1500000000 -> 1000000000 (envió 500000000)
        # Account2: 1500000000 -> 2000000000 (recibió 500000000)
        assert result.send_sol_amount == 500000000
        assert result.sol_amount == 500000000

    @pytest.mark.asyncio
    async def test_get_transaction_invalid_signature(self, mock_client):
        """Test con firma inválida."""
        with pytest.raises(ValueError, match="cadena válida"):
            await mock_client.get_transaction(signature="short")

        with pytest.raises(ValueError, match="cadena válida"):
            await mock_client.get_transaction(signature=123)

    @pytest.mark.asyncio
    async def test_get_transaction_rpc_error(self, mock_client, sample_rpc_error):
        """Test con error RPC."""
        mock_client._fetch.return_value = sample_rpc_error

        with pytest.raises(RPCException, match="Error RPC"):
            await mock_client.get_transaction(
                signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9"
            )

    @pytest.mark.asyncio
    async def test_get_transaction_not_found(self, mock_client):
        """Test cuando la transacción no existe."""
        mock_client._fetch.return_value = {"result": None}

        with pytest.raises(RPCException, match="no encontrada"):
            await mock_client.get_transaction(
                signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9"
            )

    @pytest.mark.asyncio
    async def test_get_transaction_with_options(
        self, mock_client, sample_transaction_response
    ):
        """Test con opciones de encoding y commitment."""
        mock_client._fetch.return_value = sample_transaction_response

        result = await mock_client.get_transaction(
            signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9",
            encoding="jsonParsed",
            commitment="confirmed",
        )

        assert result is not None
        call_args = mock_client._fetch.call_args
        params = call_args[1]["payload"]["params"]
        assert params[1]["encoding"] == "jsonParsed"
        assert params[1]["commitment"] == "confirmed"


class TestGetBalance:
    """Tests para el método get_balance."""

    @pytest.mark.asyncio
    async def test_get_balance_success(self, mock_client):
        """Test exitoso de get_balance."""
        mock_client._fetch.return_value = {"result": {"value": 123456789}}
        result = await mock_client.get_balance(
            pubkey="Dxu2pZyqC1YZxq5bskfDCz2gDPXPGJDQTxjJ4RPVCpnV"
        )
        assert result.value == 123456789

    @pytest.mark.asyncio
    async def test_get_balance_invalid_owner(self, mock_client):
        """Test con owner inválido."""
        with pytest.raises(ValueError, match="cadena válida"):
            await mock_client.get_balance(pubkey="")
        with pytest.raises(ValueError, match="cadena válida"):
            await mock_client.get_balance(pubkey=None)

    @pytest.mark.asyncio
    async def test_get_balance_rpc_error(self, mock_client):
        """Test con error RPC."""
        mock_client._fetch.return_value = {
            "error": {
                "code": -32602,
                "message": "Invalid params: invalid owner address",
            }
        }
        with pytest.raises(RPCException, match="Error RPC"):
            await mock_client.get_balance(
                pubkey="Dxu2pZyqC1YZxq5bskfDCz2gDPXPGJDQTxjJ4RPVCpnV"
            )

    @pytest.mark.asyncio
    async def test_get_balance_with_commitment(self, mock_client):
        """Test de get_balance con parámetro commitment."""
        mock_client._fetch.return_value = {"result": {"value": 987654321}}
        result = await mock_client.get_balance(
            pubkey="Dxu2pZyqC1YZxq5bskfDCz2gDPXPGJDQTxjJ4RPVCpnV",
            commitment="confirmed",
        )
        assert result.value == 987654321
        call_args = mock_client._fetch.call_args
        params = call_args[1]["payload"]["params"]
        assert params[0] == "Dxu2pZyqC1YZxq5bskfDCz2gDPXPGJDQTxjJ4RPVCpnV"
        assert params[1]["commitment"] == "confirmed"

    class TestGetTokenAccountsByOwner:
        """Tests para el método get_token_accounts_by_owner."""

        @pytest.mark.asyncio
        async def test_get_token_accounts_by_owner_success(
            self, mock_client, sample_get_token_accounts_by_owner_response
        ):
            """Test exitoso de get_token_accounts_by_owner."""
            mock_client._fetch.return_value = (
                sample_get_token_accounts_by_owner_response
            )

            result = await mock_client.get_token_accounts_by_owner(
                owner="DjQqV6xj8o9sKWbYYqfSXhEBUDsCdTgGwzo3wuvJgDHn",
                mint="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                commitment="confirmed",
                encoding="jsonParsed",
            )

            assert result.context.slot == 386954899
            assert len(result.value) == 1
            assert (
                result.value[0].pubkey == "3ACMdmqTvCqM6oxSqhoTauVu7VN6oogNaek7NPYmKtTk"
            )

        @pytest.mark.asyncio
        async def test_get_token_accounts_by_owner_invalid_owner(self, mock_client):
            """Owner inválido debe lanzar ValueError."""
            with pytest.raises(ValueError, match="cadena válida"):
                await mock_client.get_token_accounts_by_owner(owner="")

        @pytest.mark.asyncio
        async def test_get_token_accounts_by_owner_rpc_error(
            self, mock_client, sample_rpc_error
        ):
            """Error RPC debe lanzar RPCException."""
            mock_client._fetch.return_value = sample_rpc_error

            with pytest.raises(RPCException, match="Error RPC"):
                await mock_client.get_token_accounts_by_owner(
                    owner="DjQqV6xj8o9sKWbYYqfSXhEBUDsCdTgGwzo3wuvJgDHn",
                    mint="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                )

        @pytest.mark.asyncio
        async def test_get_token_accounts_by_owner_payload_structure(
            self, mock_client, sample_get_token_accounts_by_owner_response
        ):
            """Verifica que el payload incluye filter y options correctamente."""
            mock_client._fetch.return_value = (
                sample_get_token_accounts_by_owner_response
            )

            await mock_client.get_token_accounts_by_owner(
                owner="DjQqV6xj8o9sKWbYYqfSXhEBUDsCdTgGwzo3wuvJgDHn",
                mint="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                commitment="confirmed",
                encoding="jsonParsed",
            )

            call_args = mock_client._fetch.call_args
            payload = call_args[1]["payload"]
            assert payload["method"] == "getTokenAccountsByOwner"
            params = payload["params"]
            assert params[0] == "DjQqV6xj8o9sKWbYYqfSXhEBUDsCdTgGwzo3wuvJgDHn"
            assert params[1]["mint"] == "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
            assert params[2]["commitment"] == "confirmed"
            assert params[2]["encoding"] == "jsonParsed"
