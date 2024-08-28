from typing import Optional
from src.database.sql_connection import SQLConnection
from src.utils.logger import LOGGER
from src.utils.env import DOCKER_NETWORK
from src.utils.utils import get_network_name
from src.reputation_system.contracts.ergo import submit_reputation_proof


def update_reputation(token: str, amount: int) -> Optional[str]:
    # Take the peer_id when the token it's external. Do nothing if it's an external service.
    peer_id: str = token.split('##')[1]
    if get_network_name(ip_or_uri=token.split('##')[1]) != DOCKER_NETWORK:
        LOGGER(f"Submit reputation proof {peer_id}")
        return SQLConnection().update_reputation_peer(peer_id, amount)

def compute_reputation_feedback(peer_id) -> float:
    """
    As an initial implementation, the node will only consider its own observations.
    Therefore, it will not take into account the reputation assigned by other peers for each of the pairs it interacts with.
    """
    _result: float = SQLConnection().get_reputation(peer_id)
    LOGGER(f"Computed reputation: {_result}")
    return _result

def submit_reputation():
    SQLConnection().submit_to_ledger(
        peer_id="",
        submit=lambda proof_id, amount: submit_reputation_proof(object=proof_id, polarization=amount>0) if amount else None
    )
