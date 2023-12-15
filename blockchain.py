"""A simple blockchain implementation in Python.

UESTC4036_2023 Information Security 
Lab 1: Build a Blockchain in Python
Lab 2: Design a PoW Consensus
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
            proof (str): The proof for this block.
            data (str, optional): The data to be stored in the block.
                Defaults to 'Hello World!'.

        Returns:
            dict: The new block.
        """
        if len(self.chain) != 0:
            last_proof = self.get_previous_block()["proof"]
            if not self.valid_proof(proof, last_proof, 4):
                print("Failed to create block: Invalid proof")
                return False

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

    def proof_of_work(self, difficulty=4):
        """A simple implementation of the Proof of Work algorithm 
        inspired by the Hashcash POW, which tries different values
        of nonce to get a hash that satisfies our difficulty criteria.
        
        Note that simplfied design of the POW algorithm made use of the proof
        from the previous block instead of the date, address and other 
        information used by the Hashcash algorithm. 
         
        
        
        Args:
            difficulty (int, optional): The difficulty of the POW algorithm.
                Number of leading 0s needed. Defaults to 4.

        Returns:
            str: The proof of work.
        """
        nonce = 0
        last_proof = self.get_previous_block()["proof"]
        proof_validated = False # The control statement to check the status of the proof of work
        while not proof_validated:
            proof = str(nonce)
            proof_validated = self.valid_proof(proof, last_proof, difficulty)
            nonce += 1

        return proof

    @staticmethod
    def valid_proof(proof, last_proof, difficulty):
        """Check if a given proof is valid for the given difficulty level.

        Arguments:
            proof (str): The proof to be checked.
            difficulty (int): The difficulty level.

        Returns:
            bool: True if the proof is valid, False otherwise.
        """
        guess = f'{last_proof}{proof}'.encode()
        hash_operation = hashlib.sha256(guess).hexdigest()
        return bool(hash_operation[:difficulty] == "0" * difficulty)

    def mine_block(self, data):
        """Mines a new block in the blockchain.

        Arguments:
            data -- The data to be stored in the block.
        """
        proof = self.proof_of_work()
        self.create_block(proof, data)

    def validate_chain(self, difficulty=4):
        """Check if the previous hash of the current block is 
        the same as the hash. Also checks if the proof for each
        block is valid.
        
        Arguments:
            difficulty (int, optional): The difficulty level of the POW algorithm.
                Defaults to 4.
        
        Returns:
            bool: True if the chain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            if not self.valid_proof(current_block["proof"],
                                    previous_block["proof"],
                                    difficulty):
                # No need to check the genesis block
                return False
        return True

    def print_chain(self):
        """Prints the entire chain. """
        print("Blockchain: ")
        for index, block in enumerate(self.chain):
            print(f"Block {index}: {self.hash(block)}")
            print(block)
            print("")
