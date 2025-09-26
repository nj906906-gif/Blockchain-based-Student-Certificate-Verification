import hashlib, json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block("Genesis Certificate", "0")

    def create_block(self, certificate_data, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'certificate': certificate_data,
            'previous_hash': previous_hash,
            'hash': ''
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def hash(self, block):
        block_copy = block.copy()
        block_copy['hash'] = ''
        return hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def is_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr['previous_hash'] != prev['hash'] or curr['hash'] != self.hash(curr):
                return False
        return True

    def verify_certificate(self, cert_hash):
        return any(block['hash'] == cert_hash for block in self.chain)
