import os
import pickle
from cryptography.fernet import Fernet
from phe import paillier

class HomomorphicEncryption:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        if not os.path.exists('private_key.pkl'):
            self.generate_keys()
        else:
            self.load_keys()

    def generate_keys(self):
        """Generate new public and private key and store the private key in a pickle file"""
        # The reason why I chose key length as 4096 is it considered as extremely secure for next many decades
        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=2048)
        self.save_private_key()

    def load_keys(self):
        """Load public and private keys and assign them into object field"""
        self.private_key = self.load_private_key()
        self.public_key = self.private_key.public_key

    def save_private_key(self):
        """Save the private key into a pickle file"""
        with open("private_key.pkl", 'wb') as file:
            pickle.dump(self.private_key, file)

    def load_private_key(self):
        """Load the private key from a pickle file"""
        with open("private_key.pkl", 'rb') as file:
            private_key = pickle.load(file)
        return private_key

    def encrypt(self, value):
        """Encrypt the given value"""
        return self.public_key.encrypt(value)

    def sum(self, cipher_texts) -> int:
        """Add encrypted votes together."""
        if len(cipher_texts) == 0:
            return 0
        
        total = cipher_texts[0]
        for cipher in cipher_texts[1:]:
            total += cipher
        return self.private_key.decrypt(total)
    
    def generate_EncryptedNumber(self, cipher_number, exponent):
        return paillier.EncryptedNumber(
            self.public_key,
            cipher_number,
            exponent)


