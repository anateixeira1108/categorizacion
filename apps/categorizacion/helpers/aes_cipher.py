# -*- enconding: utf-8 -*- 

from apps.categorizacion.helpers.constants import SECRET_TAB_KEY
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 32
PADDING = '@'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
cipher = AES.new(SECRET_TAB_KEY)

encode = lambda s: base64.b64encode(cipher.encrypt(pad(s)))
decode = lambda e: cipher.decrypt(base64.b64decode(e)).rstrip(PADDING)
