"""Ejemplo de manejo de errores en RaveXRPC."""

import asyncio

from ravexrpc import RPC_Client
from ravexrpc.exceptions import RPCException


async def handle_errors_example():
    """Demuestra el manejo correcto de errores."""
    client = RPC_Client()

    # Ejemplo 1: Owner inválido
    print("1️⃣  Intentando con owner inválido:")
    try:
        await client.get_token_accounts(owner="")
    except ValueError as e:
        print(f"   ✅ Capturado ValueError: {e}\n")

    # Ejemplo 2: Firma de transacción inválida
    print("2️⃣  Intentando con firma inválida:")
    try:
        await client.get_transaction(signature="corta")
    except ValueError as e:
        print(f"   ✅ Capturado ValueError: {e}\n")

    # Ejemplo 3: Transacción no encontrada
    print("3️⃣  Intentando con firma que no existe:")
    try:
        fake_signature = "1" * 88  # Firma válida en formato pero inexistente
        await client.get_transaction(signature=fake_signature)
    except RPCException as e:
        print(f"   ✅ Capturado RPCException: {e}\n")

    # Ejemplo 4: Manejo correcto con try-except
    print("4️⃣  Ejemplo de manejo robusto:")
    owner = "InvalidAddress"

    try:
        result = await client.get_token_accounts(owner=owner)
        print(f"   ✅ Resultado: {result.total} cuentas")
    except ValueError as e:
        print(f"   ⚠️  Error de validación: {e}")
    except RPCException as e:
        print(f"   ⚠️  Error RPC: {e}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")


async def retry_with_backoff():
    """Ejemplo de reintentos con backoff exponencial."""
    client = RPC_Client()
    max_retries = 3
    base_delay = 1

    for attempt in range(max_retries):
        try:
            print(f"Intento {attempt + 1}/{max_retries}...")
            result = await client.get_token_accounts(
                owner="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"
            )
            print(f"✅ Éxito: {result.total} cuentas")
            break
        except RPCException as e:
            delay = base_delay * (2**attempt)
            print(f"⚠️  Error: {e}")

            if attempt < max_retries - 1:
                print(f"   Reintentando en {delay}s...\n")
                await asyncio.sleep(delay)
            else:
                print("❌ Máximo de reintentos alcanzado")


if __name__ == "__main__":
    print("🚀 RaveXRPC - Ejemplos de manejo de errores\n")
    print("=" * 60 + "\n")

    asyncio.run(handle_errors_example())

    print("\n" + "=" * 60)
    print("\n5️⃣  Ejemplo de reintentos con backoff exponencial:\n")

    asyncio.run(retry_with_backoff())
