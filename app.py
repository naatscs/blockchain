from flask import Flask, jsonify
from pydantic import UUID4
from blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(UUID4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "mine a new block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'lenght': len(blockchain.chain),
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)