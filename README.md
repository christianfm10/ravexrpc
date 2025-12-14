# RaveXRPC

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Cliente asíncrono para interactuar con el RPC de Solana. Proporciona una interfaz Python simple y tipo-segura para consultar información de la blockchain de Solana.

## 🚀 Características

- **Asíncrono**: Basado en `asyncio` para alto rendimiento
- **Tipo-seguro**: Utiliza Pydantic para validación de datos y tipos
- **Simple**: API intuitiva y fácil de usar
- **Extensible**: Construido sobre `ravexclient` para fácil extensión

## 📦 Instalación

Requiere Python 3.14 o superior.

```bash
# Usando uv (recomendado)
uv pip install ravexrpc

# O con pip
pip install ravexrpc
```

## 🔧 Uso

### Configuración básica

```python
import asyncio
from ravexrpc import RPC_Client

async def main():
    # Inicializar el cliente (mainnet por defecto)
    client = RPC_Client()
    
    # O especificar un endpoint personalizado
    client = RPC_Client(base_url="https://api.devnet.solana.com")
    
    # Usar el cliente
    # ...

asyncio.run(main())
```

### Obtener cuentas de tokens

```python
from ravexrpc import RPC_Client

async def get_tokens():
    client = RPC_Client()
    
    # Obtener todas las cuentas de tokens de una wallet
    result = await client.get_token_accounts(
        owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
        show_zero_balance=False,
        limit=100
    )
    
    print(f"Total de cuentas: {result.total}")
    for account in result.token_accounts:
        print(f"Token: {account.mint}")
        print(f"Balance: {account.amount}")
        print(f"Owner: {account.owner}")
    
    # Filtrar por un mint específico
    result = await client.get_token_accounts(
        owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
        mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        limit=10
    )
```

### Obtener detalles de una transacción

```python
from ravexrpc import RPC_Client

async def get_transaction():
    client = RPC_Client()
    
    # Obtener detalles de una transacción
    tx = await client.get_transaction(
        signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9",
        encoding="json",
        commitment="finalized"
    )
    
    print(f"Balances previos: {tx.meta.pre_balances}")
    print(f"Balances posteriores: {tx.meta.post_balances}")
    print(f"Cambios: {tx.meta.delta_balances}")
    
    # Calcular monto de SOL transferido
    tx = await client.get_transaction(
        signature="5wJG7K9qY1V6P9Z3Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9Y8X9",
        from_pk="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
        to_pk="8qbHbw2BbbTHBW1sbeqakYXVKRQM8Ne7pLK7m6CVfeR"
    )
    
    if tx.sol_amount:
        print(f"SOL recibido: {tx.sol_amount / 1e9} SOL")
    if tx.send_sol_amount:
        print(f"SOL enviado: {tx.send_sol_amount / 1e9} SOL")
```

## 📚 API Reference

### `RPC_Client`

Cliente principal para interactuar con el RPC de Solana.

#### Métodos

##### `get_token_accounts(owner, mint=None, show_zero_balance=False, limit=10)`

Obtiene las cuentas de tokens asociadas a una wallet.

**Parámetros:**
- `owner` (str): Dirección de la wallet (base58)
- `mint` (str, opcional): Filtrar por un token específico
- `show_zero_balance` (bool): Incluir cuentas con saldo cero (default: False)
- `limit` (int): Número máximo de resultados (default: 10)

**Retorna:** `RPCGetTokenAccountsResult`

**Excepciones:**
- `RPCException`: Error en la llamada RPC

##### `get_transaction(signature, encoding="json", commitment="finalized", from_pk=None, to_pk=None)`

Obtiene los detalles de una transacción por su firma.

**Parámetros:**
- `signature` (str): Firma de la transacción
- `encoding` (str): Formato de codificación (default: "json")
- `commitment` (str): Nivel de confirmación (default: "finalized")
- `from_pk` (str, opcional): Calcular SOL enviado desde esta dirección
- `to_pk` (str, opcional): Calcular SOL recibido en esta dirección

**Retorna:** `RPCGetTransactionResult`

**Excepciones:**
- `ValueError`: Firma inválida
- `RPCException`: Error en la llamada RPC

## 🏗️ Modelos

### `RPCGetTokenAccountsResult`

- `total` (int): Número total de cuentas
- `limit` (int): Límite de resultados
- `cursor` (str | None): Cursor para paginación
- `token_accounts` (list[RPCTokenAccounts]): Lista de cuentas

### `RPCTokenAccounts`

- `address` (str): Dirección de la cuenta
- `mint` (str): Dirección del token
- `owner` (str): Propietario de la cuenta
- `amount` (int): Balance en unidades mínimas
- `delegated_amount` (int): Cantidad delegada
- `frozen` (bool): Estado de congelación

### `RPCGetTransactionResult`

- `meta` (RPCMetaTransaction): Metadatos de la transacción
- `transaction` (RPCTransaction): Datos de la transacción
- `sol_amount` (float | None): SOL recibido (si se proporciona `to_pk`)
- `send_sol_amount` (float | None): SOL enviado (si se proporciona `from_pk`)

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
uv pip install -e ".[dev]"

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=ravexrpc --cov-report=html
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Christian Flores**
- Email: christian.flores@dekoding.pe
- GitHub: [@christianfm10](https://github.com/christianfm10)

## 🙏 Agradecimientos

- Construido sobre [ravexclient](https://github.com/christianfm10/ravexclient)
- Documentación de [Solana RPC API](https://docs.solana.com/api)
