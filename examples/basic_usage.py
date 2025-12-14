"""Ejemplo básico de uso de RaveXRPC."""

import asyncio

from ravexrpc import RPC_Client


async def get_token_accounts_example():
    # Inicializar el cliente (mainnet por defecto)
    helius_api_key = "api-key-here"  # Reemplaza con tu clave API de Helius
    client = RPC_Client(base_url=f"https://rpc.helius.xyz/?api-key={helius_api_key}")

    # Dirección de ejemplo (Solana Foundation)
    owner_address = "5zwN9NQei4fctQ8AfEk67PVoH1jSCSYCpfYkeamkpznj"

    try:
        print("🔍 Obteniendo cuentas de tokens...")
        result = await client.get_token_accounts(
            owner=owner_address,
            show_zero_balance=False,
            limit=5,
        )

        print(f"\n✅ Total de cuentas encontradas: {result.total}")
        print(f"📊 Mostrando {len(result.token_accounts)} cuentas:\n")

        for i, account in enumerate(result.token_accounts, 1):
            print(f"{i}. Token Account:")
            print(f"   Mint: {account.mint}")
            print(f"   Balance: {account.amount}")
            print(f"   Congelada: {account.frozen}")
            print()

        # Ejemplo de transacción (necesitas una firma válida)
        print("\n🔍 Ejemplo de obtener transacción:")
        print("(Requiere una firma de transacción válida)")

        # tx_signature = "tu_firma_de_transaccion_aqui"
        # tx = await client.get_transaction(signature=tx_signature)
        # print(f"Balances previos: {tx.meta.pre_balances}")
        # print(f"Balances posteriores: {tx.meta.post_balances}")
        # print(f"Cambios: {tx.meta.delta_balances}")

    except Exception as e:
        print(f"❌ Error: {e}")


async def get_balance_example():
    # Inicializar el cliente (mainnet por defecto)
    client = RPC_Client()

    # Dirección de ejemplo (Solana Foundation)
    pubkey = "5zwN9NQei4fctQ8AfEk67PVoH1jSCSYCpfYkeamkpznj"

    try:
        print("🔍 Obteniendo balance de la cuenta...")
        balance_result = await client.get_balance(pubkey=pubkey)

        print(f"\n✅ Balance de la cuenta {pubkey}: {balance_result.value / 1e9} SOL")

    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Ejemplo principal de uso del cliente RPC."""
    await get_balance_example()


if __name__ == "__main__":
    print("🚀 RaveXRPC - Ejemplo de uso\n")
    asyncio.run(main())
