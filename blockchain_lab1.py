"""A simple blockchain implementation in Python.

UESTC4036_2023 Information Security 
Lab 1: Build a Blockchain in Python
Liang Sidi & Yunke Yu, 2023
"""
import datetime
import hashlib
import json


class Blockchain:
    """A Blockchain class.

    Attributes:
        chain (list): A list of blocks.
    """

    def __init__(self):
        """Initializes the Blockchain class and creates the genesis block."""
        self.chain = []
        self.create_block(proof=0)  # Genesis Block

    def create_block(self, proof, data="Hello World!"):
        """Creates a new block and adds it to the chain

        Args:
            proof (int): The proof for this block.
                This is typically given by a Proof of Work algorithm,
                which is not implemented in this module.
            data (str, optional): The data to be stored in the block.
                Defaults to 'Hello World!'.

        Returns:
            dict: The new block.
        """
        new_block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.now().timestamp()),  # POSIX timestamp
            "data": data,
            "proof": proof,
            "previous_hash": self.get_previous_hash(),
        }
        self.chain.append(new_block)
        return new_block

    def get_previous_block(self):
        """Returns the last block in the chain.

        Returns:
            dict: The last block in the chain.
        """
        return self.chain[-1]

    def get_previous_hash(self):
        """Returns the hash of the previous block.

        Returns:
            str: The hash of the previous block or '0' if the blockchain is empty.
        """
        if len(self.chain) == 0:
            return "0"
        return self.hash(self.get_previous_block())

    def print_block(self, index):
        """Prints the block with specified index.

        Args:
            index(int): The index of the block to be printed.
        """
        print(self.chain[index])

    def hash(self, block_to_hash):
        """Hash a block using SHA-256.

        Args:
            block_to_hash (dict): The block to be hashed.

        Returns:
            str: The hash of the block.
        """
        encoded_block = json.dumps(block_to_hash, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


# Main Function
if __name__ == "__main__":
    # Task 1.1
    print("Task 1.1")
    # Create empty list
    blockchain_list = []

    # Create for loop to generate 10 blocks
    for i in range(10):
        block = {"index": i + 1, "data": list(range(100, 1001, 100))}
        blockchain_list.append(block)

    print(blockchain_list)

    # Task 1.2 and 1.3
    print("Task 1.2 and 1.3")
    blockchain = Blockchain()
    blockchain.create_block(24912, "Transaction A")
    blockchain.create_block(235714, "Transaction B")
    blockchain.print_block(0)
    blockchain.print_block(1)
    blockchain.print_block(2)
    # print(blockchain.hash(blockchain.chain[-2]))
    