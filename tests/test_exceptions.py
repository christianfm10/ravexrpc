"""Tests para el módulo exceptions."""

import pytest

from ravexrpc.exceptions import (
    InvalidAddressException,
    RPCConnectionException,
    RPCException,
    RPCTimeoutException,
    TransactionNotFoundException,
)


class TestRPCException:
    """Tests para la excepción base RPCException."""

    def test_rpc_exception_message(self):
        """Test de creación de excepción con mensaje."""
        error_msg = "Error en la llamada RPC"
        exc = RPCException(error_msg)

        assert exc.message == error_msg
        assert str(exc) == error_msg

    def test_rpc_exception_raise(self):
        """Test de lanzamiento de excepción."""
        with pytest.raises(RPCException, match="Error test"):
            raise RPCException("Error test")


class TestInvalidAddressException:
    """Tests para InvalidAddressException."""

    def test_is_rpc_exception(self):
        """Test que InvalidAddressException hereda de RPCException."""
        exc = InvalidAddressException("Dirección inválida")
        assert isinstance(exc, RPCException)

    def test_raise_invalid_address(self):
        """Test de lanzamiento de excepción."""
        with pytest.raises(InvalidAddressException, match="inválida"):
            raise InvalidAddressException("Dirección inválida")


class TestTransactionNotFoundException:
    """Tests para TransactionNotFoundException."""

    def test_is_rpc_exception(self):
        """Test que TransactionNotFoundException hereda de RPCException."""
        exc = TransactionNotFoundException("Transacción no encontrada")
        assert isinstance(exc, RPCException)

    def test_raise_transaction_not_found(self):
        """Test de lanzamiento de excepción."""
        with pytest.raises(TransactionNotFoundException, match="no encontrada"):
            raise TransactionNotFoundException("Transacción no encontrada")


class TestRPCTimeoutException:
    """Tests para RPCTimeoutException."""

    def test_is_rpc_exception(self):
        """Test que RPCTimeoutException hereda de RPCException."""
        exc = RPCTimeoutException("Timeout")
        assert isinstance(exc, RPCException)

    def test_raise_timeout(self):
        """Test de lanzamiento de excepción."""
        with pytest.raises(RPCTimeoutException, match="Timeout"):
            raise RPCTimeoutException("Timeout en la petición")


class TestRPCConnectionException:
    """Tests para RPCConnectionException."""

    def test_is_rpc_exception(self):
        """Test que RPCConnectionException hereda de RPCException."""
        exc = RPCConnectionException("Error de conexión")
        assert isinstance(exc, RPCException)

    def test_raise_connection_error(self):
        """Test de lanzamiento de excepción."""
        with pytest.raises(RPCConnectionException, match="conexión"):
            raise RPCConnectionException("Error de conexión")
