#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 00:58:04 2025

@author: madelat
"""

from blockchain2 import Blockchain  # Importamos la clase Blockchain desde blockchain2.py

# Crear una instancia de Blockchain
blockchain = Blockchain()

# Prueba 1: Minar un nuevo bloque y mostrar la blockchain
print("\n🔹 Minando un nuevo bloque...")
previous_block = blockchain.get_previous_block()
previous_proof = previous_block['proof']
proof = blockchain.proof_of_work(previous_proof)
previous_hash = blockchain.hash(previous_block)
new_block = blockchain.create_block(proof, previous_hash)

# Mostrar la información del bloque minado
print(f"\n✅ Bloque minado:\n{new_block}")

# Prueba 2: Obtener la cadena completa
print("\n🔹 Obteniendo la blockchain completa...")
for block in blockchain.chain:
    print(block)

# Prueba 3: Verificar si la blockchain es válida
print("\n🔹 Verificando la validez de la blockchain...")
is_valid = blockchain.is_chain_valid()
print(f"\n✅ ¿La blockchain es válida? {is_valid}")
