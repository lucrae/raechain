import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create genesis block
        self.create_block(previous_hash=1, proof=100)

    def create_block(self, proof, previous_hash=None):
        # create a new block in the blockchain

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])

        }

    def create_transaction(self, sender, recipient, amount):
        # create a new transaction to go into the next mined block

        self.current_transactions.apppend({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        # validate a proof to prove work

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # validate the proof

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000' # four ledaing zeroes

    @staticmethod
    def hash(block):
        # create a sha-256 hash of a block

        block_string = json.dumps(block, sort_keys=True).endcode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

# create node and create a unique address for it
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')

# instatiate the blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "mine a new block"

@app.route('/transactions/new', methods=['GET', 'POST'])
def create_transaction():
    return "create a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')