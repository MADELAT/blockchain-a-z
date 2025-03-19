#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 21:29:54 2025

@author: madelat
"""

#Versión Chatgpt 1

# Importar las librerías
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Blockchain
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.current_transactions = []  # Para almacenar transacciones futuras
        self.create_block(proof=1, previous_hash='0')  # Bloque génesis
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.datetime.now().timestamp(),  # Timestamp UNIX
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.current_transactions  # Transacciones en el bloque
        }
        self.current_transactions = []  # Reiniciar transacciones después de minar un bloque
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        """ Implementación optimizada de Proof of Work (PoW) """
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(f'{new_proof**2 - previous_proof**2}'.encode()).hexdigest()
            if hash_operation[:4] == '0000':  # Ajusta la dificultad aquí
                return new_proof
            new_proof += 1
    
    @staticmethod
    def hash(block):
        """ Calcula el hash SHA-256 de un bloque """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()    

    def is_chain_valid(self, chain):
        """ Verifica si la blockchain es válida """
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(f'{proof**2 - previous_proof**2}'.encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
            
# Parte 2 - Minado de un bloque de la blockchain

# Crear la aplicación Flask
app = Flask(__name__)

# Crear una blockchain
blockchain = Blockchain()

# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Felicidades, has minado un nuevo bloque',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }
    return jsonify(response), 200

