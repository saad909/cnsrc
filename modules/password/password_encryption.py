from cryptography.fernet import Fernet


class password_encryption:
    def encrypt_password(self, password):
        # master key
        # key = "b'QulLnMhuTxVD0ScQpRQu-imNAiG6DRu37ahnQijXzVo='"
        key = "gJXQcSqBdWK7B6uUPbifvhZJuDkoMjEHfDYb_5rvLhE="
        # generate cypher string
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        # return cypher text
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        # master key
        key = "gJXQcSqBdWK7B6uUPbifvhZJuDkoMjEHfDYb_5rvLhE="
        fernet = Fernet(key)
        # decrypt password and return

        password = fernet.decrypt(encrypted_password)
        return password.decode()
