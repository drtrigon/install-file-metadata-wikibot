#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Usage: $ invoke install_file_metadata_spm install_pywikibot install_file_metadata_bot
#
# $ sudo docker run -it drtrigon/catimages-gsoc
# # cd /opt/pywikibot-core
# # python pwb.py login.py
# # cat pywikibot.lwp
# # exit
# $ sudo docker cp `sudo docker ps -l -q`:/opt/pywikibot-core/pywikibot.lwp pywikibot.lwp
#

from __future__ import (division, absolute_import, unicode_literals,
print_function)

import sys

if (len(sys.argv) == 2) and (len(sys.argv[1]) == 32):
    open('pywikibot.lwp', 'w').write(open('pywikibot.lwp.hack', 'r').read() % {'PYWIKIBOT_TOKEN': sys.argv[1]})
