# blockchain-hash-simulation
Python simulation of blocks linked by SHA-256 hashes (TP3)
# Simulation d'une Blockchain et Chaînage Cryptographique en Python

**Auteur :** Hicham EL ABBASSI  
**Formation :** Master FinTech / Blockchain — Université Cadi Ayyad (TP3)

---

## 1. Question choisie
Comment les blocs d'une blockchain sont-ils reliés entre eux par leurs empreintes cryptographiques, et comment cette architecture permet-elle de détecter immédiatement toute tentative d'altération rétroactive des données ?

## 2. Démarche suivie
Pour répondre concrètement à cette question, j'ai développé une simulation pédagogique en Python (`blockchain_simulation.py`) reposant sur la fonction de hachage standard **SHA-256** :
1. **Modélisation d'un bloc (`Block`) :** Chaque bloc contient un index, un horodatage (*timestamp*), une liste de transactions, un `nonce` et l'empreinte cryptographique du bloc précédent (`previous_hash`).
2. **Chaînage cryptographique (`Blockchain`) :** À partir du bloc initial (*Genesis*), chaque nouveau bloc intègre dans son propre calcul de hachage l'empreinte du bloc qui le précède.
3. **Preuve de travail simplifiée :** Une difficulté configurable impose que l'empreinte du bloc commence par un nombre défini de zéros (`000...`).
4. **Audit d'intégrité (`is_chain_valid`) :** Une fonction parcourt l'ensemble de la chaîne pour recalculer l'empreinte de chaque bloc et vérifier la continuité stricte entre `previous_hash` et le `hash` du bloc précédent.

## 3. Résultat obtenu
Lors de l'exécution du script (`python blockchain_simulation.py`) :
- **État sain :** Les blocs `#0`, `#1` et `#2` sont générés et liés. Le `Hash précédent` de chaque bloc correspond exactement au `Hash actuel` du bloc précédent, et la vérification renvoie `True`.
- **Test d'altération :** Dès qu'une transaction du Bloc `#1` est modifiée (`2.5 BTC` remplacé par `250.0 BTC`), son empreinte SHA-256 change radicalement. La méthode `is_chain_valid()` détecte immédiatement l'incohérence et retourne `False`, démontrant l'immuabilité pratique du registre.

## 4. Outils utilisés
- **Langage :** Python 3 (modules standard `hashlib`, `json`, `time`).
- **Gestion de versions :** Git et GitHub Desktop.
- **Assistance IA :** Utilisation d'un assistant d'intelligence artificielle (Gemini) pour la structuration pédagogique du code Python et la mise en forme de la documentation Markdown, avec relecture et tests complets par l'auteur.

## 5. Sources
- Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System* (Section 2 : Transactions et Section 3 : Timestamp Server).
- Documentation officielle Python — Module `hashlib` (Secure hashes and message digests) : https://docs.python.org/3/library/hashlib.html
- Documentation GitHub Desktop : https://docs.github.com/en/desktop