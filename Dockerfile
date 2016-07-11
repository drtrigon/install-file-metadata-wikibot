############################################################
# Dockerfile to build gsoc-catimages container image
# Based on Ubuntu resp. file_metadata_0.1.0.dev99999999999999
############################################################

# Set the base image to Ubuntu
FROM drtrigon/file_metadata_0.1.0.dev99999999999999

# File Author / Maintainer
MAINTAINER DrTrigon <dr.trigon@surfeu.ch>

# Update the repository sources list
RUN apt-get update

################## BEGIN INSTALLATION ######################
# Install gsoc-catimages Following the Instructions at Wikipedia Commons
# Ref: https://commons.wikimedia.org/wiki/User:DrTrigon/file-metadata

# Installation of file-metadata
RUN ln -s /opt/file-metadata/tests tests

# Installation of pywikibot
RUN git clone --branch 2.0 --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /opt/pywikibot-core
RUN ln -s /opt/pywikibot-core/pywikibot pywikibot

# Setup of simple_bot.py
RUN apt-get -y install libmagickwand-dev

# Setup of bulk.py
RUN apt-get install python-opencv
RUN pip install retry httplib2 --upgrade
RUN wget https://raw.githubusercontent.com/AbdealiJK/file-metadata/95cc2abb3506608266b1faf0da0722433ad6b03b/tests/bulk.py

# Run tests here ... may be do unittests or run a bot script
RUN echo "RUN simple_bot.py BY ENTERING:"
RUN echo "cd /opt/pywikibot-core/; python pwb.py basic; cd /"
RUN echo "cd /opt/pywikibot-core; python pwb.py ../file-metadata/file_metadata/wikibot/simple_bot.py -cat:SVG_files -limit:5; cd /"
RUN echo "RUN bulk.py BY ENTERING:"
RUN echo "cd /opt/pywikibot-core/; python pwb.py basic; cd /"
RUN echo "python bulk.py -search:'eth-bib' -limit:5 -logname:test -dryrun:1 -dir:/opt/pywikibot-core/"

##################### INSTALLATION END #####################
