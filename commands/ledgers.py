from typing import Generator, List
from commands.__interface import table_command
from contracts.eth_main.utils import check_provider_availability
from src.utils.utils import get_ledgers, get_ledger_providers
import ecdsa
import binascii


def private_key_to_public_key(private_key: str) -> str:

    private_key = private_key[2:]  # Remove the '0x' prefix
    # TODO change the algorithm between ledgers

    # Decodificar la clave privada hexadecimal
    private_key_bytes = binascii.unhexlify(private_key)

    # Obtener la clave pública correspondiente a partir de la clave privada
    signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    public_key = signing_key.verifying_key.to_string()

    # Codificar la clave pública como una cadena hexadecimal
    public_key_hex = binascii.hexlify(public_key).decode('utf-8')
    return public_key_hex


def generator() -> Generator[List[str], None, None]:
    for ledger_id, private_key in get_ledgers():
        yield [
            ledger_id,
            private_key_to_public_key(private_key),
            private_key,
            str(any(check_provider_availability(i) for i in get_ledger_providers(ledger=ledger_id)))
        ]


def ledgers(stream: bool = True):
    table_command(
        f=generator,
        headers=[
            'LEDGER',
            'PUBLIC KEY',
            'PRIVATE KEY',
            'AVALIABLE'
        ],
        stream=stream
    )


def view(ledger: str):
    from database.query_interface import fetch_query
    private_key: str = next(fetch_query(
        query="SELECT private_key FROM ledger WHERE id = ?",
        params=(ledger,)
    ))[0]
    print(f"LEDGER -> {ledger}")
    print(f"PUBLIC KEY -> {private_key_to_public_key(private_key)}")
    print(f"PRIVATE KEY -> {private_key}")