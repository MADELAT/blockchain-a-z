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
        """ Inicializa la Blockchain con el bloque génesis """
        self.chain = []
        self.create_block(proof=1, previous_hash='0')  # Crear el primer bloque

    def create_block(self, proof, previous_hash):
        """ Crea un nuevo bloque y lo añade a la cadena """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        """ Devuelve el último bloque de la Blockchain """
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        """ 
        Implementación del Proof of Work (PoW) 
        Se busca un número (new_proof) que, al pasarlo por SHA-256 junto con el previous_proof,
        genere un hash con los primeros 4 caracteres en '0000'. 
        """
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':  # Ajustar la dificultad agregando más ceros
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        """ Calcula el hash de un bloque """
        encoded_block = json.dumps(block, sort_keys=True).encode()  # Se corrigió el espacio en sort_keys
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        """ Verifica si la blockchain es válida """
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]

            # Verificar que el previous_hash del bloque actual coincide con el hash del bloque anterior
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Verificar que el proof_of_work es válido
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True  # Si pasó todas las validaciones, la blockchain es válida
