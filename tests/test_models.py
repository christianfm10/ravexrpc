"""Tests para el módulo models."""

import pytest
from pydantic import ValidationError

from ravexrpc.models import (
    RPCGetBalanceResult,
    RPCGetTokenAccountsResult,
    RPCGetTransactionResult,
    RPCMessageModel,
    RPCMetaTransaction,
    RPCTokenAccounts,
    RPCTransaction,
)


class TestRPCTokenAccounts:
    """Tests para el modelo RPCTokenAccounts."""

    def test_valid_token_account(self):
        """Test de creación de cuenta de token válida."""
        account = RPCTokenAccounts(
            address="TokenAddress",
            mint="MintAddress",
            owner="OwnerAddress",
            amount=1000000,
            delegated_amount=0,
            frozen=False,
        )

        assert account.address == "TokenAddress"
        assert account.amount == 1000000
        assert not account.frozen

    def test_negative_amount_validation(self):
        """Test de validación de montos negativos."""
        with pytest.raises(ValidationError, match="no negativos"):
            RPCTokenAccounts(
                address="TokenAddress",
                mint="MintAddress",
                owner="OwnerAddress",
                amount=-1000,
                delegated_amount=0,
                frozen=False,
            )


class TestRPCGetTokenAccountsResult:
    """Tests para el modelo RPCGetTokenAccountsResult."""

    def test_valid_result(self):
        """Test de resultado válido."""
        result = RPCGetTokenAccountsResult(
            total=2,
            limit=10,
            cursor=None,
            token_accounts=[
                RPCTokenAccounts(
                    address="Address1",
                    mint="Mint1",
                    owner="Owner1",
                    amount=1000,
                    delegated_amount=0,
                    frozen=False,
                ),
                RPCTokenAccounts(
                    address="Address2",
                    mint="Mint2",
                    owner="Owner2",
                    amount=2000,
                    delegated_amount=0,
                    frozen=False,
                ),
            ],
        )

        assert result.total == 2
        assert len(result.token_accounts) == 2

    def test_negative_total_validation(self):
        """Test de validación de total negativo."""
        with pytest.raises(ValidationError, match="no negativos"):
            RPCGetTokenAccountsResult(
                total=-1,
                limit=10,
                cursor=None,
                token_accounts=[],
            )


class TestRPCMetaTransaction:
    """Tests para el modelo RPCMetaTransaction."""

    def test_delta_balance_calculation(self):
        """Test de cálculo automático de delta_balances."""
        meta = RPCMetaTransaction(
            preBalances=[1000000000, 2000000000, 3000000000],
            postBalances=[1500000000, 1500000000, 3500000000],
        )

        assert meta.delta_balances == [500000000, -500000000, 500000000]

    def test_mismatched_balances_length(self):
        """Test con longitudes diferentes de balances."""
        with pytest.raises(ValidationError, match="misma longitud"):
            RPCMetaTransaction(
                preBalances=[1000000000, 2000000000],
                postBalances=[1500000000],
            )


class TestRPCGetTransactionResult:
    """Tests para el modelo RPCGetTransactionResult."""

    def test_valid_transaction(self):
        """Test de transacción válida."""
        tx = RPCGetTransactionResult(
            meta=RPCMetaTransaction(
                preBalances=[1000000000, 2000000000],
                postBalances=[1500000000, 1500000000],
            ),
            transaction=RPCTransaction(
                message=RPCMessageModel(accountKeys=["Account1", "Account2"])
            ),
        )

        assert tx.meta.delta_balances == [500000000, -500000000]

    def test_sol_amount_calculation_to_pk(self):
        """Test de cálculo de SOL recibido con to_pk."""
        tx = RPCGetTransactionResult(
            meta=RPCMetaTransaction(
                preBalances=[1000000000, 2000000000],
                postBalances=[1500000000, 2500000000],
            ),
            transaction=RPCTransaction(
                message=RPCMessageModel(accountKeys=["Account1", "Account2"])
            ),
            to_pk="Account2",
        )

        # Account2: 2000000000 -> 2500000000 (recibió 500000000)
        assert tx.sol_amount == 500000000

    def test_sol_amount_calculation_from_pk(self):
        """Test de cálculo de SOL enviado con from_pk."""
        tx = RPCGetTransactionResult(
            meta=RPCMetaTransaction(
                preBalances=[2000000000, 1000000000],
                postBalances=[1500000000, 1500000000],
            ),
            transaction=RPCTransaction(
                message=RPCMessageModel(accountKeys=["Account1", "Account2"])
            ),
            from_pk="Account1",
        )

        # Account1: 2000000000 -> 1500000000 (envió 500000000)
        assert tx.send_sol_amount == 500000000

    def test_sol_amount_with_invalid_to_account(self):
        """Test con cuenta que no existe en account_keys."""
        tx = RPCGetTransactionResult(
            meta=RPCMetaTransaction(
                preBalances=[1000000000, 2000000000],
                postBalances=[1500000000, 1500000000],
            ),
            transaction=RPCTransaction(
                message=RPCMessageModel(accountKeys=["Account1", "Account2"])
            ),
            to_pk="NonExistentAccount",
        )

        assert tx.sol_amount is None

    def test_sol_amount_with_invalid_from_account(self):
        """Test con cuenta que no existe en account_keys."""
        tx = RPCGetTransactionResult(
            meta=RPCMetaTransaction(
                preBalances=[1000000000, 2000000000],
                postBalances=[1500000000, 1500000000],
            ),
            transaction=RPCTransaction(
                message=RPCMessageModel(accountKeys=["Account1", "Account2"])
            ),
            from_pk="NonExistentAccount",
        )

        assert tx.send_sol_amount is None

    def test_str_representation(self):
        """Test de representación string del modelo."""
        tx = RPCGetTransactionResult(
            meta=RPCMetaTransaction(
                preBalances=[1000000000],
                postBalances=[2000000000],
            ),
            transaction=RPCTransaction(
                message=RPCMessageModel(accountKeys=["Account1"])
            ),
        )

        str_repr = str(tx)
        assert "meta" in str_repr
        assert "transaction" in str_repr
        # Debe ser JSON formateado
        assert "\n" in str_repr


class TestRPCGetBalanceResult:
    """Tests para el modelo RPCGetBalanceResult."""

    def test_valid_balance(self):
        """Test de balance válida."""
        tx = RPCGetBalanceResult(value=100000)

        assert tx.value == 100000
