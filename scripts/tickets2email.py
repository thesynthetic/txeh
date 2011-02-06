#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import stat
import datetime

from gluon.utils import md5_hash
from gluon.restricted import RestrictedError
from gluon.tools import Mail


path = os.path.join(request.folder, 'errors')
hashes = {}
mail = Mail()

### CONFIGURE HERE
SLEEP_MINUTES = 5
ALLOW_DUPLICATES = True
mail.settings.server = 'localhost:25'
mail.settings.sender = 'you@localhost'
administrator_email = 'you@localhost'
### END CONFIGURATION

while 1:
    for file in os.listdir(path):
        filename = os.path.join(path, file)

        if not ALLOW_DUPLICATES:
            file_data = open(filename, 'r').read()
            key = md5_hash(file_data)

            if key in hashes:
                continue

            hashes[key] = 1

        error = RestrictedError()
        error.load(request, request.application, filename)

        mail.send(to=administrator_email, subject='new web2py ticket', message=error.traceback)
        
        os.unlink(filename)
    time.sleep(SLEEP_MINUTES * 60)
