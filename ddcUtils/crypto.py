# -*- encoding: utf-8 -*-
import base64
import os
from cryptography.fernet import Fernet, InvalidToken


class Cryptography:
    def __init__(self, private_key: str = None):
        self.private_key = private_key or "sMZo38VwRdigN78FBnHj8mETNlofL4Qhj_x5cvyxJsc="
        try:
            self.cipher_suite = Fernet(bytes(self.private_key, "UTF-8"))
        except ValueError as e:
            raise ValueError(str(e))

    @staticmethod
    def generate_private_key() -> str:
        """
        Generates a private key to be used instead of default one
        But keep in mind that this private key will be needed to decode further strings
        :return: str
        """
        private_key = base64.urlsafe_b64encode(os.urandom(32))
        return private_key.decode("UTF-8")

    def encode(self, str_to_encode: str) -> str:
        """
        Encodes a given string
        :param str_to_encode:
        :return: str
        """
        str_bytes = bytes(str_to_encode, "UTF-8")
        encoded_text = self.cipher_suite.encrypt(str_bytes)
        return encoded_text.decode("UTF-8")

    def decode(self, str_to_decode: str) -> str:
        """
        Decodes a given string
        :param str_to_decode:
        :return:
        """
        if str_to_decode is not None and len(str_to_decode) > 0:
            try:
                bet = bytes(str_to_decode, "UTF-8")
                decoded_text = self.cipher_suite.decrypt(bet).decode("UTF-8")
                return str(decoded_text)
            except InvalidToken:
                error_msg = "Not encrypted"
                if len(str_to_decode) == 100:
                    error_msg = "Encrypted with another private key"
                raise InvalidToken(error_msg)
