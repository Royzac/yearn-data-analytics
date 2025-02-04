import pytest
from dotenv import load_dotenv
from src.yearn import Network, Web3Provider

load_dotenv()

USDC_VAULT = (Network.Mainnet, "0xa354F35829Ae975e850e23e9615b11Da1B3dC4DE")
WFTM_VAULT = (Network.Fantom, "0x0DEC85e74A92c52b7F708c4B10207D9560CEFaf0")


@pytest.mark.parametrize("network, address", [USDC_VAULT, WFTM_VAULT])
def test_fetch_abi(network, address):
    w3 = Web3Provider(network)
    abi = w3.fetch_abi(address)
    assert any([f["name"] == "Transfer" for f in abi])


@pytest.mark.parametrize("network, address", [USDC_VAULT, WFTM_VAULT])
def test_call(network, address):
    w3 = Web3Provider(network)
    value = w3.call(address, "performanceFee")
    assert value == 2000


@pytest.mark.parametrize("num_blocks", [10000])
@pytest.mark.parametrize("network, address", [USDC_VAULT, WFTM_VAULT])
def test_fetch_events(network, address, num_blocks):
    w3 = Web3Provider(network)
    current_block = w3.provider.eth.get_block_number()
    from_block = current_block - num_blocks
    events = w3.fetch_events(address, "Transfer", from_block)
    assert len(events) > 0


@pytest.mark.parametrize("num_blocks", [10000])
@pytest.mark.parametrize("network, address", [USDC_VAULT, WFTM_VAULT])
def test_erc20_tokens(network, address, num_blocks):
    w3 = Web3Provider(network)
    current_block = w3.provider.eth.get_block_number()
    from_block = current_block - num_blocks
    addresses = w3.erc20_tokens(address, from_block)
    assert len(addresses) > 0


USDC_MAINNET = (Network.Mainnet, "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
USDC_FANTOM = (Network.Fantom, "0x04068da6c83afcfa0e13ba15a6696662335d5b75")


@pytest.mark.parametrize("network, address", [USDC_MAINNET, USDC_FANTOM])
def test_get_usdc_price(network, address):
    w3 = Web3Provider(network)
    assert w3.get_usdc_price(address) > 0


@pytest.mark.parametrize("network, address", [USDC_MAINNET, USDC_FANTOM])
def test_get_labels(network, address):
    w3 = Web3Provider(network)
    labels = w3.get_scan_labels(address)
    assert "Token Contract" in labels
