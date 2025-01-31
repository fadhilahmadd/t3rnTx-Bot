from web3 import Web3
from eth_account import Account
import time
import sys

from data_bridge import data_bridge
from keys_and_addresses import private_keys, my_addresses, labels
from network_config import networks

chain_symbols = {
    'Arbitrum Sepolia': '\033[34m',   
    'OP Sepolia': '\033[91m',         
    'Base Sepolia': '\033[96m'       
}

green_color = '\033[92m'
reset_color = '\033[0m'

explorer_urls = {
    'Arbitrum Sepolia': 'https://sepolia.arbiscan.io/tx/',
    'OP Sepolia': 'https://sepolia-optimism.etherscan.io/tx/',
    'Base Sepolia': 'https://sepolia.basescan.org/tx/',
    'BRN': 'https://brn.explorer.caldera.xyz/tx/'
}

def get_brn_balance(web3, my_address):
    balance = web3.eth.get_balance(my_address)
    return web3.from_wei(balance, 'ether')

def send_bridge_transaction(web3, account, my_address, data, network_name):
    nonce = web3.eth.get_transaction_count(my_address, 'pending')
    value_in_ether = 0.8
    value_in_wei = web3.to_wei(value_in_ether, 'ether')

    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': networks[network_name]['contract_address'],
            'from': my_address,
            'data': data,
            'value': value_in_wei
        })
        gas_limit = gas_estimate + 50000 
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

    base_fee = web3.eth.get_block('latest')['baseFeePerGas']
    priority_fee = web3.to_wei(5, 'gwei')
    max_fee = base_fee + priority_fee

    transaction = {
        'nonce': nonce,
        'to': networks[network_name]['contract_address'],
        'value': value_in_wei,
        'gas': gas_limit,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': priority_fee,
        'chainId': networks[network_name]['chain_id'],
        'data': data
    }

    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        balance = web3.eth.get_balance(my_address)
        formatted_balance = web3.from_wei(balance, 'ether')

        explorer_link = f"{explorer_urls[network_name]}{web3.to_hex(tx_hash)}"

        print(f"{green_color}📤 Alamat Pengirim: {account.address}")
        print(f"⛽ Gas digunakan: {tx_receipt['gasUsed']}")
        print(f"🗳️  Nomor blok: {tx_receipt['blockNumber']}")
        print(f"💰 Saldo ETH: {formatted_balance} ETH")
        brn_balance = get_brn_balance(Web3(Web3.HTTPProvider('https://brn.rpc.caldera.xyz/http')), my_address)
        print(f"🔵 Saldo BRN: {brn_balance} BRN")
        print(f"🔗 Link Explorer: {explorer_link}\n{reset_color}")

        return web3.to_hex(tx_hash), value_in_ether
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None, None

def process_network_transactions(network_name, bridges, chain_data, successful_txs):
    web3 = Web3(Web3.HTTPProvider(chain_data['rpc_url'], request_kwargs={'timeout': 60}))
    if not web3.is_connected():
        raise Exception(f"Tidak dapat terhubung ke jaringan {network_name}")

    for bridge in bridges:
        for i, private_key in enumerate(private_keys):
            account = Account.from_key(private_key)
            data = data_bridge[bridge]
            result = send_bridge_transaction(web3, account, my_addresses[i], data, network_name)
            if result:
                tx_hash, value_sent = result
                successful_txs += 1

                # Check if value_sent is valid before formatting
                if value_sent is not None:
                    print(f"{chain_symbols[network_name]}🚀 Total Tx Sukses: {successful_txs} | {labels[i]} | Bridge: {bridge} | Jumlah Bridge: {value_sent:.5f} ETH ✅{reset_color}\n")
                else:
                    print(f"{chain_symbols[network_name]}🚀 Total Tx Sukses: {successful_txs} | {labels[i]} | Bridge: {bridge} ✅{reset_color}\n")

                print(f"{'='*150}")
                print("\n")
            time.sleep(8) 

    return successful_txs

def main():
    successful_txs = 0

    while True:
        try:
            for i, private_key in enumerate(private_keys):
                account = Account.from_key(private_key)
                web3_op = Web3(Web3.HTTPProvider(networks['OP Sepolia']['rpc_url']))
                if not web3_op.is_connected():
                    raise Exception(f"Tidak dapat terhubung ke jaringan OP Sepolia")

                balance_op = web3_op.eth.get_balance(my_addresses[i])
                formatted_balance_op = web3_op.from_wei(balance_op, 'ether')

                if formatted_balance_op <= 1.0:
                    print(f"{chain_symbols['OP Sepolia']}⚠️  Saldo tidak mencukupi untuk {labels[i]} di OP Sepolia. Saldo saat ini: {formatted_balance_op:.5f} ETH ⚠️{reset_color}\n")
                    continue  # Skip this address if balance is <= 1.0 ETH

                # Process transactions for OP Sepolia if balance is sufficient
                successful_txs = process_network_transactions('OP Sepolia', ["OP - ARB", "OP - BASE"], networks['OP Sepolia'], successful_txs)
                time.sleep(3)

            for i, private_key in enumerate(private_keys):
                account = Account.from_key(private_key)
                web3_arb = Web3(Web3.HTTPProvider(networks['Arbitrum Sepolia']['rpc_url']))
                if not web3_arb.is_connected():
                    raise Exception(f"Tidak dapat terhubung ke jaringan Arbitrum Sepolia")

                balance_arb = web3_arb.eth.get_balance(my_addresses[i])
                formatted_balance_arb = web3_arb.from_wei(balance_arb, 'ether')

                if formatted_balance_arb <= 1.0:
                    print(f"{chain_symbols['Arbitrum Sepolia']}⚠️  Saldo tidak mencukupi untuk {labels[i]} di Arbitrum Sepolia. Saldo saat ini: {formatted_balance_arb:.5f} ETH ⚠️{reset_color}\n")
                    continue  # Skip this address if balance is <= 1.0 ETH

                # Process transactions for Arbitrum Sepolia if balance is sufficient
                successful_txs = process_network_transactions('Arbitrum Sepolia', ["ARB - OP SEPOLIA", "ARB - BASE"], networks['Arbitrum Sepolia'], successful_txs)
                time.sleep(3)

            for i, private_key in enumerate(private_keys):
                account = Account.from_key(private_key)
                web3_base = Web3(Web3.HTTPProvider(networks['Base Sepolia']['rpc_url']))
                if not web3_base.is_connected():
                    raise Exception(f"Tidak dapat terhubung ke jaringan Base Sepolia")

                balance_base = web3_base.eth.get_balance(my_addresses[i])
                formatted_balance_base = web3_base.from_wei(balance_base, 'ether')

                if formatted_balance_base <= 1.0:
                    print(f"{chain_symbols['Base Sepolia']}⚠️  Saldo tidak mencukupi untuk {labels[i]} di Base Sepolia. Saldo saat ini: {formatted_balance_base:.5f} ETH ⚠️{reset_color}\n")
                    continue  # Skip this address if balance is <= 1.0 ETH

                # Process transactions for Base Sepolia if balance is sufficient
                successful_txs = process_network_transactions('Base Sepolia', ["BASE - OP", "BASE - ARB"], networks['Base Sepolia'], successful_txs)
                time.sleep(3)

        except KeyboardInterrupt:
            print("\nScript dihentikan oleh pengguna. ✋")
            print(f"Total transaksi sukses: {successful_txs} 🎉")
            sys.exit(0)

if __name__ == "__main__":
    main()