# -*- coding: utf8 -*-

import rsa
import re
import six


class RSAKey:
    def __init__(self):
        """
        "empty" RSA key constructor
        """
        self.n = None
        self.e = 0
        self.d = None
        self.p = None
        self.q = None
        self.dmp1 = None
        self.dmq1 = None
        self.coeff = None

    def setPublic(self, N, E):
        """
        Set the public key fields N and e from hex strings
        """
        if N is not None and E is not None and len(N) > 0 and len(E) > 0:
            self.n = int(N, 16)
            self.e = int(E, 16)
        else:
            raise ValueError

    def encrypt(self, text):
        """
        Return the PKCS#1 RSA encryption of "text" as an even-length hex string
        """
        if text is None:
            return None
        pubkey = rsa.PublicKey(self.n, self.e)
        text = text.encode("utf8")
        ciphertext = rsa.encrypt(text, pubkey)
        if six.PY3:
            return ''.join([("%x" % x).zfill(2) for x in ciphertext])
        else:
            return ''.join([("%x" % ord(x)).zfill(2) for x in ciphertext])

    def setPrivate(self, N, E, D):
        """
        Set the private key fields N, e, and d from hex strings
        """
        if N is not None and E is not None and len(N) > 0 and len(E) > 0:
            self.n = int(N, 16)
            self.e = int(E, 16)
            self.d = int(D, 16)
        else:
            raise ValueError

    def setPrivateEx(self, N, E, D, P, Q, DP, DQ, C):
        """
        Set the private key fields N, e, d and CRT params from hex strings
        """
        if N is not None and E is not None and len(N) > 0 and len(E) > 0:
            self.n = int(N, 16)
            self.e = int(E, 16)
            self.d = int(D, 16)
            self.p = int(P, 16)
            self.q = int(Q, 16)
            self.dmp1 = int(DP, 16)
            self.dmq1 = int(DQ, 16)
            self.coeff = int(C, 16)

        else:
            raise ValueError

    def decrypt(self, ctext):
        """
        Return the PKCS#1 RSA decryption of "ctext".
        "ctext" is an even-length hex string and the output is a plain string.
        """

        ctext = bytearray([int(x, 16) for x in re.findall(r'\w\w', ctext)])
        prikey = rsa.PrivateKey(self.n, self.e, self.d, self.p, self.q,
                                self.dmp1, self.dmq1, self.coeff)

        return rsa.decrypt(ctext, prikey).decode("utf-8")

    def generate(self, B, E):
        """
        Generate a new random private key B bits long, using public expt E
        """
        self.e = int(E, 16)
        (pubkey, prikey) = rsa.newkeys(B)
        self.n = pubkey.n
        self.e = pubkey.e
        self.d = prikey.d
        self.p = prikey.p
        self.q = prikey.q
        self.dmp1 = prikey.exp1
        self.dmq1 = prikey.exp2
        self.coeff = prikey.coef


