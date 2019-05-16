import base64
import binascii
from OpenSSL import crypto


class PKCS12(object):
    def __init__(self, file, pwd):
        """
        :param file: bytes
        :param pwd: str
        """
        self.p12 = crypto.load_pkcs12(file, pwd)

    def get_privatekey(self):
        """
        获取私钥
        :return: str
        """
        return crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                      self.p12.get_privatekey())

    def get_certificate(self):
        """
        获取证书
        :return: hex
        """
        pem = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                      self.p12.get_certificate())
        pem = pem.replace(b'-----BEGIN CERTIFICATE-----\n', b'')
        pem = pem.replace(b'\n-----END CERTIFICATE-----\n', b'')
        b64_data = base64.b64decode(pem)
        return binascii.b2a_hex(b64_data).decode()


class X509(object):
    def __init__(self, file):
        """
        :param file: bytes stream
        """
        self.cert = crypto.load_certificate(crypto.FILETYPE_ASN1, file)

    def get_pubkey(self):
        """
        获取公钥
        :return: str
        """
        a = self.cert.get_pubkey()
        pubk = crypto.dump_publickey(crypto.FILETYPE_PEM, a)
        # pubk = binascii.b2a_hex(b).decode()
        return pubk.decode('GBK')