import hashlib
import json
import time


class Block:
    """Représente un bloc individuel dans la blockchain."""

    def __init__(self, index: int, transactions: list, previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calcule l'empreinte cryptographique SHA-256 du bloc."""
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        # sort_keys=True garantit un ordre déterministe pour le hachage
        block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Applique une preuve de travail simplifiée (hash commençant par N zéros)."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    """Gère la chaîne de blocs et vérifie son intégrité cryptographique."""

    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """Crée le premier bloc de la chaîne (bloc Genesis)."""
        genesis = Block(0, ["Bloc Genesis - Initialisation du registre"], "0" * 64)
        genesis.mine_block(self.difficulty)
        return genesis

    def get_latest_block(self) -> Block:
        """Retourne le dernier bloc validé de la chaîne."""
        return self.chain[-1]

    def add_block(self, transactions: list) -> None:
        """Crée, mine et ajoute un nouveau bloc relié au bloc précédent."""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=previous_block.hash,
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """Vérifie que chaque bloc est intègre et correctement relié au précédent."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 1. Vérifier que les données du bloc n'ont pas été altérées
            if current_block.hash != current_block.calculate_hash():
                print(f"[ALERTE] L'empreinte du bloc #{current_block.index} ne correspond plus à son contenu !")
                return False

            # 2. Vérifier le chaînage avec l'empreinte du bloc précédent
            if current_block.previous_hash != previous_block.hash:
                print(f"[ALERTE] Rupture du lien cryptographique entre le bloc #{previous_block.index} et #{current_block.index} !")
                return False

            # 3. Vérifier la preuve de travail
            if current_block.hash[: self.difficulty] != "0" * self.difficulty:
                print(f"[ALERTE] Preuve de travail invalide pour le bloc #{current_block.index} !")
                return False

        return True


if __name__ == "__main__":
    print("=== 1. INITIALISATION DE LA BLOCKCHAIN ===")
    ma_blockchain = Blockchain(difficulty=3)

    print("Ajout du Bloc #1...")
    ma_blockchain.add_block(["Alice envoie 2.5 BTC à Bob", "Bob envoie 0.4 BTC à Charlie"])

    print("Ajout du Bloc #2...")
    ma_blockchain.add_block(["Charlie envoie 1.0 BTC à Diana"])

    print("\n=== 2. ÉTAT DE LA CHAÎNE DE BLOCS ===")
    for bloc in ma_blockchain.chain:
        print(f"Bloc #{bloc.index}")
        print(f"  Transactions   : {bloc.transactions}")
        print(f"  Hash précédent : {bloc.previous_hash}")
        print(f"  Hash actuel    : {bloc.hash}")
        print(f"  Nonce          : {bloc.nonce}\n")

    print(f"Intégrité de la chaîne avant altération : {ma_blockchain.is_chain_valid()}")

    print("\n=== 3. SIMULATION D'UNE TENTATIVE DE FRAUDE ===")
    print("Modification frauduleuse de la transaction du Bloc #1...")
    ma_blockchain.chain[1].transactions = ["Alice envoie 250.0 BTC à Bob"]

    print(f"Intégrité de la chaîne après altération : {ma_blockchain.is_chain_valid()}")