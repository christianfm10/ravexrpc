"""Cliente RPC para interactuar con la blockchain de Solana."""

from typing import Literal

from ravexclient import BaseClient

from ravexrpc.exceptions import RPCException
from ravexrpc.models import (
    RPCGetBalanceResult,
    RPCGetTokenAccountsByOwnerResult,
    RPCGetTokenAccountsResult,
    RPCGetTransactionResult,
)

# Tipos de encoding soportados por Solana RPC
EncodingType = Literal["json", "jsonParsed", "base58", "base64"]
# Niveles de commitment soportados
CommitmentLevel = Literal["processed", "confirmed", "finalized"]


class RPC_Client(BaseClient):
    """Cliente para interactuar con el RPC de Solana.

    Este cliente proporciona métodos para consultar información de la blockchain
    de Solana, incluyendo cuentas de tokens y transacciones.

    Attributes:
        BASE_URL: URL por defecto del RPC de Solana mainnet-beta

    Example:
        >>> async with RPC_Client() as client:
        ...     result = await client.get_token_accounts(owner="...")
        ...     print(f"Total cuentas: {result.total}")
    """

    BASE_URL = "https://api.mainnet-beta.solana.com"

    def __init__(
        self,
        base_url: str = "https://api.mainnet-beta.solana.com",
        timeout: float = 5.0,
    ):
        """Inicializa el cliente RPC de Solana.

        Args:
            base_url: URL del endpoint RPC de Solana. Por defecto usa mainnet-beta.
            timeout: Tiempo máximo de espera para las peticiones en segundos.
                Por defecto 30 segundos.

        Example:
            >>> # Usar mainnet (por defecto)
            >>> client = RPC_Client()
            >>>
            >>> # Usar devnet
            >>> client = RPC_Client(base_url="https://api.devnet.solana.com")
            >>>
            >>> # Con timeout personalizado
            >>> client = RPC_Client(timeout=60.0)
        """
        super().__init__(base_url=base_url, timeout=timeout)

    async def get_token_accounts(
        self,
        owner: str,
        mint: str | None = None,
        show_zero_balance: bool = False,
        limit: int = 10,
    ) -> RPCGetTokenAccountsResult:
        """Obtiene las cuentas de tokens asociadas a una wallet.

        Args:
            owner: Dirección de la wallet propietaria (formato base58).
            mint: Dirección del mint del token para filtrar resultados.
                Si es None, retorna todas las cuentas de tokens. Por defecto None.
            show_zero_balance: Si True, incluye cuentas con balance cero.
                Por defecto False.
            limit: Número máximo de cuentas a retornar. Por defecto 10.

        Returns:
            Objeto RPCGetTokenAccountsResult conteniendo:
                - total: Número total de cuentas encontradas
                - limit: Límite aplicado
                - cursor: Cursor para paginación (si existe)
                - token_accounts: Lista de cuentas de tokens

        Raises:
            ValueError: Si la dirección del owner es inválida.
            RPCException: Si ocurre un error en la llamada RPC.

        Example:
            >>> # Obtener todas las cuentas
            >>> result = await client.get_token_accounts(
            ...     owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"
            ... )
            >>>
            >>> # Filtrar por un token específico
            >>> result = await client.get_token_accounts(
            ...     owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
            ...     mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            ... )
        """
        if not owner or not isinstance(owner, str):
            raise ValueError("La dirección del owner debe ser una cadena válida")

        method = "getTokenAccounts"
        params = {
            "limit": limit,
            "owner": owner,
            "options": {
                "showZeroBalance": show_zero_balance,
            },
        }

        # Solo añadir mint si se proporciona
        if mint is not None:
            params["mint"] = mint

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        result = await self._fetch("POST", payload=payload)

        if "error" in result:
            error_msg = result["error"].get("message", "Error desconocido")
            raise RPCException(f"Error RPC: {error_msg}")

        return RPCGetTokenAccountsResult(**result["result"])

    async def get_transaction(
        self,
        signature: str,
        encoding: EncodingType = "json",
        commitment: CommitmentLevel = "finalized",
        from_pk: str | None = None,
        to_pk: str | None = None,
    ) -> RPCGetTransactionResult:
        """Obtiene los detalles de una transacción por su firma.

        Args:
            signature: Firma de la transacción (formato base58).
            encoding: Formato de codificación de la respuesta. Por defecto "json".
                Opciones: "json", "jsonParsed", "base58", "base64".
            commitment: Nivel de confirmación de la transacción.
                Por defecto "finalized". Opciones: "processed", "confirmed", "finalized".
            from_pk: Dirección del remitente para calcular SOL enviado. Opcional.
            to_pk: Dirección del destinatario para calcular SOL recibido. Opcional.

        Returns:
            Objeto RPCGetTransactionResult conteniendo:
                - meta: Metadatos de la transacción (balances, fees, etc.)
                - transaction: Datos de la transacción (mensaje, firmas, etc.)
                - sol_amount: SOL recibido en to_pk (si se proporciona)
                - send_sol_amount: SOL enviado desde from_pk (si se proporciona)

        Raises:
            ValueError: Si la firma es inválida (demasiado corta o no es string).
            RPCException: Si ocurre un error en la llamada RPC o la transacción
                no se encuentra.

        Example:
            >>> # Obtener transacción básica
            >>> tx = await client.get_transaction(
            ...     signature="5wJG7K9qY1V6P9Z3Y8X9..."
            ... )
            >>>
            >>> # Calcular SOL transferido
            >>> tx = await client.get_transaction(
            ...     signature="5wJG7K9qY1V6P9Z3Y8X9...",
            ...     from_pk="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
            ...     to_pk="8qbHbw2BbbTHBW1sbeqakYXVKRQM8Ne7pLK7m6CVfeR"
            ... )
            >>> print(f"SOL enviado: {tx.send_sol_amount / 1e9} SOL")
        """
        if not isinstance(signature, str) or len(signature) < 20:
            raise ValueError(
                "La firma debe ser una cadena válida de al menos 20 caracteres"
            )

        method = "getTransaction"
        params = [
            signature,
            {
                "commitment": commitment,
                "encoding": encoding,
                "maxSupportedTransactionVersion": 0,
            },
        ]
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        result = await self._fetch("POST", payload=payload)

        if "error" in result:
            error_msg = result["error"].get("message", "Error desconocido")
            raise RPCException(f"Error RPC: {error_msg}")

        if result.get("result") is None:
            raise RPCException(f"Transacción no encontrada: {signature}")

        return RPCGetTransactionResult(
            **result["result"],
            from_pk=from_pk,
            to_pk=to_pk,
        )

    async def get_token_accounts_by_owner(
        self,
        owner: str,
        mint: str | None = None,
        commitment: CommitmentLevel = "finalized",
        encoding: EncodingType = "jsonParsed",
    ) -> RPCGetTokenAccountsByOwnerResult:
        """Consulta `getTokenAccountsByOwner` del RPC de Solana.

        Construye el payload en formato de lista de parámetros que acepta
        el endpoint y retorna un modelo tipado con la respuesta.

        Args:
            owner: Dirección del owner (base58).
            mint: Mint del token para filtrar (opcional).
            commitment: Nivel de confirmación (processed|confirmed|finalized).
            encoding: Encoding de la respuesta (jsonParsed|json|base58|base64).

        Returns:
            RPCGetTokenAccountsByOwnerResult con `context` y `value` (lista de cuentas).

        Raises:
            ValueError: Si `owner` no es válido.
            RPCException: Si el RPC responde con error.
        """
        if not owner or not isinstance(owner, str):
            raise ValueError("La dirección del owner debe ser una cadena válida")

        method = "getTokenAccountsByOwner"

        # Parametros: [owner, filterObject, options]
        filter_obj = {"mint": mint} if mint is not None else {}
        options = {"commitment": commitment, "encoding": encoding}
        params = [owner, filter_obj or {}, options]

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        result = await self._fetch("POST", payload=payload)

        if "error" in result:
            error_msg = result["error"].get("message", "Error desconocido")
            raise RPCException(f"Error RPC: {error_msg}")

        return RPCGetTokenAccountsByOwnerResult(**result["result"])

    async def get_balance(
        self,
        pubkey: str,
        commitment: CommitmentLevel = "finalized",
    ) -> RPCGetBalanceResult:
        """Obtiene el balance de una cuenta en lamports.

        Args:
            pubkey: Dirección de la cuenta (formato base58).
            commitment: Nivel de confirmación para consultar el balance.
                Por defecto "finalized". Opciones: "processed", "confirmed", "finalized".

        Returns:
            Balance de la cuenta en lamports (RPCGetBalanceResult).

        Raises:
            ValueError: Si la dirección es inválida.
            RPCException: Si ocurre un error en la llamada RPC.

        Example:
            >>> balance = await client.get_balance(
            ...     pubkey="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"
            ... )
            >>> print(f"Balance: {balance / 1e9} SOL")
        """
        if not pubkey or not isinstance(pubkey, str):
            raise ValueError("La dirección de la cuenta debe ser una cadena válida")

        method = "getBalance"
        params = [pubkey, {"commitment": commitment}]
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        result = await self._fetch("POST", payload=payload)

        if "error" in result:
            error_msg = result["error"].get("message", "Error desconocido")
            raise RPCException(f"Error RPC: {error_msg}")

        return RPCGetBalanceResult(**result["result"])
