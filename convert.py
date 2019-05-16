def form2json(form_data):
    from urllib.parse import parse_qs, urlparse
    query = urlparse('?' + form_data).query
    params = parse_qs(query)
    res_msg = {key: params[key][0] for key in params}
    return res_msg


def hex3b64(server_pubk):
    # str <- b64 <- hex
    import base64
    import binascii
    return base64.b64encode(
        binascii.unhexlify(server_pubk.encode('GBK'))).decode('GBK')


def str2hex(b64_data):
    import binascii
    return binascii.b2a_hex(b64_data).decode()

