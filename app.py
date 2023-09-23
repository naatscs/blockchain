from flask import Flask, jsonify
from pydantic import UUID4
from blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(UUID4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transactios(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New block forged!",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    request = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in request for k in required):
        return 'Missing values', 400
    
    index = blockchain.new_transactios( request['sender'],
                                        request['recipient'],
                                        request['amount'])
    response = {'message': f'Transaction will be added to block {index}'}

    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'lenght': len(blockchain.chain),
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)