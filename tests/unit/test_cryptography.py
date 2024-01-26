# -*- encoding: utf-8 -*-
from cryptography.fernet import InvalidToken
import pytest
from ddcUtils import Cryptography


class TestCryptography:
    @classmethod
    def setup_class(cls):
        cls.private_key = "sMZo38VwRdigN78FBnHj8mETNlofL4Qhj_x5cvyxJsc="

    @classmethod
    def teardown_class(cls):
        pass

    def test_generate_private_key(self):
        crypto = Cryptography()
        result = crypto.generate_private_key()
        assert result is not None

    def test_encode_str(self):
        str_to_encode = "test"
        crypto = Cryptography(self.private_key)
        result = crypto.encode(str_to_encode)
        assert result is not None

    def test_encode_int(self):
        to_encode = 1
        crypto = Cryptography(self.private_key)
        with pytest.raises(TypeError) as exc_info:
            crypto.encode(to_encode)
        assert exc_info.value.args[0] == "encoding without a string argument"
        assert exc_info.typename == "TypeError"

    def test_decode(self):
        passw = "gAAAAABls-0f8Krl0SGvMrcJWv3fpa8cUfkcqb-yivz6KZS4jb0-N6K2AGkwq8GkVa5Btfpht9hiVVLcF8v0Vwj0_U2o799QbQ=="
        crypto = Cryptography(self.private_key)
        result = crypto.decode(passw)
        assert result == "test"

    def test_decode_wrong_private_key(self):
        not_valid_private_key = "not a private key"
        with pytest.raises(ValueError) as exc_info:
            Cryptography(not_valid_private_key)
        assert exc_info.value.args[0] == "Fernet key must be 32 url-safe base64-encoded bytes."
        assert exc_info.typename == "ValueError"

    def test_decode_not_encrypted(self):
        passw = "not encrypted password"
        crypto = Cryptography(self.private_key)
        with pytest.raises(InvalidToken) as exc_info:
            crypto.decode(passw)
        assert exc_info.value.args[0] == "Not encrypted"
        assert exc_info.typename == "InvalidToken"

    def test_decode_mismatch_private_key(self):
        wrong_private_key = "wN3dIm9VeT_dtDi1rQoJVehdmUtG_lIFyGRGv9p4cAs="
        passw = "gAAAAABls-0f8Krl0SGvMrcJWv3fpa8cUfkcqb-yivz6KZS4jb0-N6K2AGkwq8GkVa5Btfpht9hiVVLcF8v0Vwj0_U2o799QbQ=="
        crypto = Cryptography(wrong_private_key)
        with pytest.raises(InvalidToken) as exc_info:
            crypto.decode(passw)
        assert exc_info.value.args[0] == "Encrypted with another private key"
        assert exc_info.typename == "InvalidToken"
