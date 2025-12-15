"""RaveXRPC - Cliente asíncrono para el RPC de Solana.

Este paquete proporciona una interfaz Python tipo-segura y fácil de usar
para interactuar con el RPC de Solana.

Example:
    >>> import asyncio
    >>> from ravexrpc import RPC_Client
    >>>
    >>> async def main():
    ...     async with RPC_Client() as client:
    ...         result = await client.get_token_accounts(
    ...             owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"
    ...         )
    ...         print(f"Total cuentas: {result.total}")
    >>>
    >>> asyncio.run(main())
"""

from ravexrpc.client import RPC_Client
from ravexrpc.exceptions import (
    InvalidAddressException,
    RPCConnectionException,
    RPCException,
    RPCTimeoutException,
    TransactionNotFoundException,
)
from ravexrpc.models import (
    RPCGetBalanceResult,
    RPCGetTokenAccountsByOwnerResult,
    RPCGetTokenAccountsResult,
    RPCGetTransactionResult,
    RPCMessageModel,
    RPCMetaTransaction,
    RPCResponse,
    RPCTokenAccounts,
    RPCTransaction,
)

__version__ = "0.1.0"

__all__ = [
    # Cliente principal
    "RPC_Client",
    # Excepciones
    "RPCException",
    "InvalidAddressException",
    "TransactionNotFoundException",
    "RPCTimeoutException",
    "RPCConnectionException",
    # Modelos de respuesta
    "RPCGetTokenAccountsResult",
    "RPCGetTokenAccountsByOwnerResult",
    "RPCGetBalanceResult",
    "RPCGetTransactionResult",
    "RPCTokenAccounts",
    "RPCMetaTransaction",
    "RPCTransaction",
    "RPCMessageModel",
    "RPCResponse",
]


def main() -> None:  # pragma: no cover
    """Función principal para CLI (placeholder)."""
    print("RaveXRPC v0.1.0 - Cliente RPC para Solana")
    print("Para más información, visita: https://github.com/christianfm10/ravexrpc")
