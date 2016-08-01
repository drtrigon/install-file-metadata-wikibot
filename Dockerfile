############################################################
# Dockerfile to build gsoc-catimages container image
# Based on ubuntu:14.04 resp. file-metadata
############################################################

# Set the base image
FROM pywikibotcatfiles/file-metadata

# File Author / Maintainer
MAINTAINER DrTrigon <dr.trigon@surfeu.ch>

# Set the python encoding (bugfix: UnicodeEncodeError)
ENV PYTHONIOENCODING UTF-8

# Update the repository sources list
RUN apt-get update

################## BEGIN INSTALLATION ######################
# Install gsoc-catimages Following the Instructions at Wikipedia Commons
# Ref: https://commons.wikimedia.org/wiki/User:DrTrigon/file-metadata

# Installation of file-metadata
RUN ln -s /opt/file-metadata/tests tests

# Installation of pywikibot
RUN git clone --branch 2.0 --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /opt/pywikibot-core && \
  ln -s /opt/pywikibot-core/pywikibot pywikibot

# Setup of simple_bot.py
RUN apt-get -y install libmagickwand-dev

# Setup of bulk.py
RUN apt-get install python-opencv
RUN pip install retry httplib2 --upgrade
#RUN wget https://raw.githubusercontent.com/AbdealiJK/file-metadata/95cc2abb3506608266b1faf0da0722433ad6b03b/tests/bulk.py
#RUN wget https://raw.githubusercontent.com/pywikibot-catfiles/file-metadata/ajk/work/file_metadata/wikibot/bulk_bot.py
ADD https://raw.githubusercontent.com/pywikibot-catfiles/file-metadata/ajk/work/file_metadata/wikibot/bulk_bot.py .

##################### INSTALLATION END #####################

ADD user-config.py /opt/pywikibot-core/
# hacky login.py replacemement:
ADD pywikibot.lwp.hack /opt/pywikibot-core/
ADD login-hack.py /opt/pywikibot-core/

# Show some info about the docker image
RUN echo "\n" \
"RUN simple_bot.py BY ENTERING: \n" \
"  cd /opt/pywikibot-core; python pwb.py ../file-metadata/file_metadata/wikibot/simple_bot.py -cat:SVG_files -limit:5; cd / \n" \
"RUN bulk.py BY ENTERING: \n" \
"  python bulk_bot.py -search:'eth-bib' -limit:5 -logname:test -dryrun:1 -dir:/opt/pywikibot-core/ \n"
