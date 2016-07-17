#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hi There!
# This script serves for the purpose of installing a testing environment to a
# Kubuntu VirtualBox guest as described in User:DrTrigon/file-metadata:
# https://commons.wikimedia.org/wiki/User:DrTrigon/file-metadata
#
# Usage: $ invoke install_file_metadata_spm install_pywikibot install_file_metadata_bot
#        $ invoke install_file_metadata_pip install_pywikibot install_file_metadata_bot
#        $ invoke install_pywikibot install_file_metadata_git (install_file_metadata_bot)
#        $ invoke install_pywikibot --yes install_file_metadata_git --yes
#        $ invoke install_docker --yes
#
# Inspired by https://github.com/pypa/get-pip/blob/master/get-pip.py
#         and http://www.pyinvoke.org/
#
# Performance Analysis (Time and Memory Profiling):
# * https://www.huyng.com/posts/python-performance-analysis
#
# * http://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
# * https://zapier.com/engineering/profiling-python-boss/
# * https://pymotw.com/2/profile/
# * https://julien.danjou.info/blog/2015/guide-to-python-profiling-cprofile-concrete-case-carbonara
#   -> generate stats and graphs
#
# * http://www.vrplumber.com/programming/runsnakerun/
#   -> generate stats and graphs
# * (https://pypi.python.org/pypi/meliae)

from __future__ import (division, absolute_import, unicode_literals,
print_function)

from invoke import task
#from functools import wraps
import logging, inspect

logging.basicConfig(
#    filename = fileName,
#    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    format = "%(levelname) -10s %(asctime)s %(message)s",
#    level = logging.DEBUG
    level = logging.INFO
)
cmdno = 0

# Install procedure
def run(ctx, job, yes=False):
    global cmdno
    for cmd in job:
        print("\n" + ("--- " * 18))
        lvl = 0
        for item in inspect.stack()[1:][::-1]:
            if 'catimages-gsoc/tasks.py' not in item[1]:
                continue
            lvl += 1
            logging.info("%s> %s:%s" % (("-"*lvl), item[3], item[2]))
        cmdno += 1
        logging.info("Step %i : %s" % (cmdno, cmd))
        print("--- " * 18)
        if not yes:
            raw_input("[Enter] to continue or [Ctrl]+C to stop ...")
        ctx.run(cmd)

# Parameter procesing
def params(*args, **kwargs):
    kwargs['yes'] = '--yes' if kwargs['yes'] else ''
    return kwargs

## Decorator for disabling tasks
#def disabled(func):
#    @wraps(func)
#    def decorated(ctx, *args, **kwargs):
#        print("\n" + ("--- " * 18))
#        logging.info("DISABLED : %s" % func)
#        print("--- " * 18)
#        #return func(ctx, *args, **kwargs)
#        #return (lambda ctx, *args, **kwargs: None)
#        return (lambda: None)
#    return decorated

# Function for disabling tasks
def disabled(func):
    print("\n" + ("--- " * 18))
    logging.info("DISABLED : %s" % func)
    print("--- " * 18)

# Test through system package management
@task
def install_file_metadata_spm(ctx, yes=False):
    install_pip(ctx, yes=yes)
    install_file_metadata_deps_spm(ctx, yes=yes)
    install_file_metadata(ctx, yes=yes)

def install_pip(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo apt-get %(yes)s update" % p,
    "sudo apt-get %(yes)s purge python-pip; sudo apt-get %(yes)s autoremove" % p,
    "wget https://bootstrap.pypa.io/get-pip.py; sudo python get-pip.py",
    "pip show pip",
    ]
    run(ctx, job, yes=yes)

def install_file_metadata_deps_spm(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo apt-get %(yes)s install python-appdirs python-magic python-numpy python-scipy python-matplotlib python-wand python-skimage python-zbar cmake libboost-python-dev liblzma-dev libjpeg-dev libz-dev" % p,
    ]
    run(ctx, job, yes=yes)

def install_file_metadata(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo pip install file-metadata --upgrade",
    "python -c'import file_metadata; print file_metadata.__version__'",
    ]
    run(ctx, job, yes=yes)

# Test through pip
@task
def install_file_metadata_pip(ctx, yes=False):
    install_pip(ctx, yes=yes)
    install_file_metadata_deps_pip(ctx, yes=yes)
    install_file_metadata(ctx, yes=yes)

def install_file_metadata_deps_pip(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo apt-get %(yes)s install perl openjdk-7-jre python-dev pkg-config libfreetype6-dev libpng12-dev liblapack-dev libblas-dev gfortran cmake libboost-python-dev liblzma-dev libjpeg-dev python-virtualenv" % p,
    ]
    run(ctx, job, yes=yes)

# Test through github
@task
def install_file_metadata_git(ctx, yes=False):
    install_pip(ctx, yes=yes)
    install_file_metadata_deps_pip(ctx, yes=yes)
    p   = params(yes=yes)
    job = [
    "git clone https://github.com/AbdealiJK/file-metadata.git",
    "sudo apt-get %(yes)s install libzbar-dev" % p,
    "sudo apt-get %(yes)s install libimage-exiftool-perl libav-tools" % p,
    "cd file-metadata/; sudo pip install . --upgrade",
    "cd file-metadata/; python -c'import file_metadata; print file_metadata.__version__'",
    "cd core/; ln -s ../file-metadata/file_metadata file_metadata",
    ]
    run(ctx, job, yes=yes)

# Installation of pywikibot
@task
def install_pywikibot(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo apt-get %(yes)s update" % p,
    "sudo apt-get %(yes)s install git git-review" % p,
    "git clone --branch 2.0 --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git",
    ]
    run(ctx, job, yes=yes)
    configure_pywikibot(ctx, yes=yes)

# Test bot script
@task
def install_file_metadata_bot(ctx, yes=False):
    p   = params(yes=yes)
    job = [
#    "sudo apt-get %(yes)s install libmagickwand-dev" % p,
    "cd core/; wget https://raw.githubusercontent.com/pywikibot-catfiles/file-metadata/master/file_metadata/wikibot/simple_bot.py",
    ]
    run(ctx, job, yes=yes)

# Install Docker container
@task
def install_docker(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo apt-get %(yes)s update" % p,
    "sudo apt-get %(yes)s upgrade" % p,
    "sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D" % p,
    "echo \"deb https://apt.dockerproject.org/repo ubuntu-trusty main\" | sudo tee /etc/apt/sources.list.d/docker.list" % p,
    "sudo apt-get %(yes)s update" % p,
    "sudo apt-get %(yes)s install docker-engine" % p,
    #"sudo service docker start" % p,
    ]
    run(ctx, job, yes=yes)
    configure_docker(ctx, yes=yes)

# Configuration of pywikibot
@task
def configure_pywikibot(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    #"cd core/; python pwb.py basic",    # issue: ctx.run stops after this line
    "cd core/; wget https://raw.githubusercontent.com/drtrigon/catimages-gsoc/master/user-config.py",
    ]
    run(ctx, job, yes=yes)

# Configuration of docker for running tests
@task
def configure_docker(ctx, yes=False):
    p   = params(yes=yes)
    job = [
    "sudo docker pull drtrigon/catimages-gsoc",
    ]
    run(ctx, job, yes=yes)

# Test of pywikibot-catfiles scripts (and file-metadata)
@task
def test_script(ctx, yes=False, git=False):
#    test_script_simple_bot(ctx, yes=yes, git=git)
    test_script_bulk(ctx, yes=yes, git=git)
# !!!TODO: should be runned first (see above), but since it has an error and the other not atm I swapped them temporarily
    test_script_simple_bot(ctx, yes=yes, git=git)

def test_script_simple_bot(ctx, yes=False, git=False):
    p   = params(yes=yes)
    if not git:
        job = [
    "cd core/; python pwb.py simple_bot.py -cat:SVG_files -limit:5",
    ]
    else:
        job = [
    "locale",
    "sudo dpkg-reconfigure locales",  # generate locales
    #"locale-gen de_CH.UTF-8",
    "locale",
#    "export LC_ALL=de_CH.UTF-8",      # set locale
#    "export LANG=de_CH.UTF-8",
#    "export LANGUAGE=de_CH.UTF-8",
#    #"export LANGUAGE=de_CH:de",
    "export LC_ALL=en_GB.UTF-8",      # set locale
    "export LANG=en_GB.UTF-8",
    "export LANGUAGE=en_GB.UTF-8",
    #"export LANGUAGE=en_GB:en",
    "locale",
    "source ~/.bashrc",
    "locale",                         # check locale setting
    "cd core/; python pwb.py file_metadata/wikibot/simple_bot.py -cat:SVG_files -limit:5",
    ]
    run(ctx, job, yes=yes)

def test_script_bulk(ctx, yes=False, git=False):
    p   = params(yes=yes)
    job = [
    "sudo apt-get install python-opencv",
    "cd core/; wget https://raw.githubusercontent.com/pywikibot-catfiles/file-metadata/ajk/work/file_metadata/wikibot/bulk_bot.py",
    ]
    if git:
        job += [
    "cd core/ && wget https://raw.githubusercontent.com/drtrigon/catimages-gsoc/master/pywikibot.lwp.hack",
    "cd core/ && wget https://raw.githubusercontent.com/drtrigon/catimages-gsoc/master/login-hack.py",
    "cd core/ && python login-hack.py $PYWIKIBOT_TOKEN",
    "cd core/ && python pwb.py login.py",
    ]
    job += [
    #"cd core/; python bulk_bot.py -search:'eth-bib' -limit:5 -logname:test -dryrun:1",
    "cd core/; python bulk_bot.py -search:'eth-bib' -limit:5 -logname:test",
    "sudo pip install line_profiler memory_profiler",
    "cd core/; python -m cProfile bulk_bot.py -search:'eth-bib' -limit:5 -logname:test",
    "cd core/; kernprof -l -v bulk_bot.py -search:'eth-bib' -limit:5 -logname:test && python -m line_profiler bulk_bot.py.lprof ",
    "cd core/; python -m memory_profiler bulk_bot.py -search:'eth-bib' -limit:5 -logname:test",
    ]
    run(ctx, job, yes=yes)

# Test of docker image contained scripts
@task
def test_docker(ctx, yes=False):
    p   = params(yes=yes)
#    p['travis'] = '-i' if travis else '-it'
    p['travis'] = '-i'  # use -i instead of -it due to tty
    job = [
#    "sudo docker run %(travis)s drtrigon/catimages-gsoc bash -c \"cd /opt/pywikibot-core && python pwb.py ../file-metadata/file_metadata/wikibot/simple_bot.py -cat:SVG_files -limit:5 && cd /\"" % p,
# hacky login.py replacement:
# !!!ISSUE: make 'login.py -pass:xxx' work or use -oauth token
# !!!TODO: need a way to run bulk_bot.py w/o needing to enter a passwd, e.g. like -simulate
    #"sudo docker run %(travis)s drtrigon/catimages-gsoc bash -c \"python bulk.py -search:'eth-bib' -limit:5 -logname:test -dryrun:1 -dir:/opt/pywikibot-core/\"" % p,
    "sudo docker run %(travis)s drtrigon/catimages-gsoc bash -c \"cd /opt/pywikibot-core && python login-hack.py $PYWIKIBOT_TOKEN && " \
      "cd /opt/pywikibot-core && python pwb.py login.py\"" % p,  # check login
    "sudo docker run %(travis)s drtrigon/catimages-gsoc bash -c \"cd /opt/pywikibot-core && python login-hack.py $PYWIKIBOT_TOKEN && " \
      "cd /; python bulk_bot.py -search:'eth-bib' -limit:5 -logname:test -dir:/opt/pywikibot-core/\"" % p,
#    "sudo docker run %(travis)s drtrigon/catimages-gsoc bash -c \"cd /opt/pywikibot-core && python pwb.py /bulk_bot.py -search:'eth-bib' -limit:5 -logname:test -dir:/opt/pywikibot-core/\"" % p,
# !!!TODO: should be runned first (see above), but since it has an error and the other not atm I swapped them temporarily
    "sudo docker run %(travis)s drtrigon/catimages-gsoc bash -c \"cd /opt/pywikibot-core && python pwb.py ../file-metadata/file_metadata/wikibot/simple_bot.py -cat:SVG_files -limit:5 && cd /\"" % p,

# docker:
#
# unittests
# coverage
# https://github.com/pywikibot-catfiles/file-metadata/blob/master/.travis.yml#L60
# script:
#   - flake8 setup.py setupdeps.py file_metadata tests
#   - python -m pytest --cov ;
#   - python setup.py sdist bdist bdist_wheel
    ]
    run(ctx, job, yes=yes)
