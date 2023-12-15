"""A simple blockchain implementation in Python.

UESTC4036_2023 Information Security 
Lab 2: Design a PoW Consensus
Liang Sidi & Yunke Yu, 2023
"""
from blockchain import Blockchain

# Main function
if __name__ == "__main__":
    bc = Blockchain() # Create a blockchain
    # Mine two blocks
    bc.mine_block("Transaction A")
    bc.mine_block("Transaction B")
    bc.print_chain()
    # Validate teh blockchain
    if bc.validate_chain():
        print("Blockchain is valid")
    else:
        print("Blockchain is invalid")
