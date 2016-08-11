#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# "hacky login.py replacement"
# !!!ISSUE: make 'login.py -pass:xxx' work or use -oauth token
#
# Usage: $ python login-hack.py $PYWIKIBOT_TOKEN
#
# $ sudo docker run -it drtrigon/catimages-gsoc
# # cd /opt/pywikibot-core
# # python pwb.py login.py
# # cat pywikibot.lwp
# # exit
# $ sudo docker cp `sudo docker ps -l -q`:/opt/pywikibot-core/pywikibot.lwp \
#     pywikibot.lwp.hack
# replace 'centralauth_Token=...;' by 'centralauth_Token=%(PYWIKIBOT_TOKEN)s;'
#   in pywikibot.lwp.hack and commit then push
#
# See also: Dockerfile, tasks.py
#

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import sys

if (len(sys.argv) == 2) and (len(sys.argv[1]) == 32):
    open('pywikibot.lwp', 'w').write(open('pywikibot.lwp.hack', 'r').read() %
                                     {'PYWIKIBOT_TOKEN': sys.argv[1]})
