from phe import paillier

# Generate Paillier public and private keys
public_key, private_key = paillier.generate_paillier_keypair()



# Numbers to be encrypted
numbers = [5.5, 3.2, 7.8]

# Encrypt the numbers
encrypted_numbers = [public_key.encrypt(num) for num in numbers]
print("Encrypted Numbers: ", encrypted_numbers)

cipher = encrypted_numbers[0].ciphertext()
print(cipher)
print(cipher.to_bytes(64,byteorder="big"))

# # Perform homomorphic addition on encrypted numbers
# encrypted_sum = encrypted_numbers[0]
# for enc_num in encrypted_numbers[1:]:
#     print(str(enc_num.exponent))
#     encrypted_sum += enc_num

# # Decrypt the result
# decrypted_sum = private_key.decrypt(encrypted_sum)
# print("Decrypted sum:", decrypted_sum)

# from cryptography.fernet import Fernet

# encrpytor = Fernet(Fernet.generate_key())

# cipher1 = encrpytor.encrypt("1".encode())
# cipher2 = encrpytor.encrypt("1000000000000000000000000".encode())

# print(cipher1)
# print(cipher2)

# print(encrpytor.decrypt(cipher1))
# print(encrpytor.decrypt(cipher2))