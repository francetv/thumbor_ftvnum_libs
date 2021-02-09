# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
from thumbor.url_signers import BaseUrlSigner
#from six import text_type
#from libthumbor.url_signers import BaseUrlSigner
from thumbor.utils import deprecated, logger


class UrlSigner(BaseUrlSigner):
    """Validate urls and sign them using base64 hmac-sha1
    """

    def signature(self, url):
        oas= base64.urlsafe_b64encode(
            hmac.new(
                self.security_key, str(url).encode('utf-8'), hashlib.sha1
            ).digest()
        )
        oad = oas.decode('utf8').replace('=', '').encode()
        return oad
