import cryptography


class password_encryption:
    def encrypt_password(self, password):
        # master key
        key = "3940042f9de617fb53189cfc97d6251dedc23420e5aeb4042f1f6186fd6d27a9"
        # generate cypher string
        fernet = Fernet(key)

        encrypted_password = fernet.encrypt(message.encode())
        # return cypher text
        return encrypted_password()

    def decrypt_password(self, encrypted_password):
        # master key
        key = "3940042f9de617fb53189cfc97d6251dedc23420e5aeb4042f1f6186fd6d27a9"
        fernet = Fernet(key)
        # decrypt password and return
        password = fernet.decrypt(encMessage).decode()
        return password
