import threading
import hashlib
import time
import copy

class Block:
    def __init__(self, data):
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Calcula o hash do bloco usando o hashlib
        block_string = str(self.data).encode()
        return hashlib.sha256(block_string).hexdigest()

# Bloco original salvo
original_block = Block("Dados iniciais do bloco")
shared_block = copy.deepcopy(original_block)

# Lock para garantir que as threads não acessem o bloco ao mesmo tempo
block_lock = threading.Lock()

def block_validator():
    while True:
        time.sleep(2)  # Verifica a cada 2 segundos
        with block_lock:
            if shared_block.hash != original_block.calculate_hash():
                print("Alteração detectada! Bloco inválido. Descartando o bloco modificado...")
                # Reverte o bloco para o original
                shared_block.data = original_block.data
                shared_block.hash = original_block.hash
            else:
                print("Bloco válido. Nenhuma alteração detectada.")

def modify_block():
    while True:
        time.sleep(5)  # Modifica o bloco a cada 5 segundos
        with block_lock:
            shared_block.data = "Dados modificados do bloco"
            shared_block.hash = shared_block.calculate_hash()
            print("Bloco modificado!")

# Cria as threads
validator_thread = threading.Thread(target=block_validator)
modifier_thread = threading.Thread(target=modify_block)

# Inicia as threads
validator_thread.start()
modifier_thread.start()

# Aguarda as threads finalizarem (nunca vai acontecer)
validator_thread.join()
modifier_thread.join()