#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hi There!
# This script serves for the purpose of installing a testing environment to a
# Kubuntu VirtualBox guest as described in User:DrTrigon/file-metadata:
# https://commons.wikimedia.org/wiki/User:DrTrigon/file-metadata
#
# Usage:
# $ invoke install_file_metadata_spm install_pywikibot
# $ invoke install_file_metadata_pip install_pywikibot
# $ invoke install_file_metadata_git install_pywikibot
# $ invoke install_file_metadata_git --yes install_pywikibot --yes
# $ invoke install_docker --yes
#
# Inspired by https://github.com/pypa/get-pip/blob/master/get-pip.py
#         and http://www.pyinvoke.org/
#
# Syntax and Coverage:
# * Syntax: pyflake/flake8 (PEP8)
# * (unittests)
# * (coverage)
# -> $ cd file-metadata; python -m pytest --cov
#
# Performance Analysis (Time and Memory Profiling):
# * https://www.huyng.com/posts/python-performance-analysis
# * http://milianw.de/blog/heaptrack-a-heap-memory-profiler-for-linux
#
# * http://stackoverflow.com/questions/582336/ \
#     how-can-you-profile-a-python-script
# * https://zapier.com/engineering/profiling-python-boss/
# * https://pymotw.com/2/profile/
# * https://julien.danjou.info/blog/2015/ \
#     guide-to-python-profiling-cprofile-concrete-case-carbonara
#   -> generate stats and graphs
# * valgrind
#   http://svn.python.org/projects/python/trunk/Misc/valgrind-python.supp
#   $ valgrind --tool=massif --suppressions=valgrind-python.supp [prog]
#   http://valgrind.org/docs/manual/ms-manual.html
#   "If the output file format string (controlled by --massif-out-file) does
#   not contain %p, then the outputs from the parent and child will be
#   intermingled in a single output file, which will almost certainly make it
#   unreadable by ms_print."
#
# * http://www.vrplumber.com/programming/runsnakerun/
#   -> generate stats and graphs
# * (https://pypi.python.org/pypi/meliae)

from __future__ import (division, absolute_import, unicode_literals,
    print_function)

from invoke import task
#from functools import wraps
import logging
import inspect

logging.basicConfig(
    #filename=fileName,
    #format="%(levelname) -10s %(asctime)s %(module)s:%(lineno)s "
    #       "%(funcName)s %(message)s",
    format="%(levelname) -10s %(asctime)s %(message)s",
    #level=logging.DEBUG
    level=logging.INFO
)
cmdno = 0

#TRAVIS = os.environ.get('CI', False) or \
#         os.environ.get('TRAVIS', False)


# Install procedure
def run(ctx, job, yes=False):
    global cmdno
    for cmd in job:
        print("\n" + ("--- " * 18))
        lvl = 0
        for item in inspect.stack()[1:][::-1]:
#            if 'catimages-gsoc/tasks.py' not in item[1]:
            if '/tasks.py' not in item[1]:
                continue
            lvl += 1
            logging.info("%s> %s:%s" % (("-" * lvl), item[3], item[2]))
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
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s update" % p,
        # install most recent pip
        # assume pip to be already installed
        "sudo pip install -U pip",
        "pip show pip",
        # install spm setup dependencies
        "sudo apt-get %(yes)s install python-appdirs python-magic "
          "python-numpy python-scipy python-matplotlib python-wand "
          "python-skimage python-zbar cmake libboost-python-dev "
          "liblzma-dev libjpeg-dev libz-dev" % p,
        # install additional dependencies for pip build
        "sudo apt-get %(yes)s install libzbar-dev" % p,
        "sudo apt-get %(yes)s install libimage-exiftool-perl libav-tools" % p,
        # install file-metadata through pip only
        "sudo pip install file-metadata --upgrade",
        # test import of file-metadata
        "python -c'import file_metadata; print(file_metadata.__version__)'",
    ]
    run(ctx, job, yes=yes)


# Test through pip
@task
def install_file_metadata_pip(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s update" % p,
        # install most recent pip
        # assume pip to be already installed
        "sudo pip install -U pip",
        "pip show pip",
        # install pip setup dependencies
        "sudo apt-get %(yes)s install perl openjdk-7-jre python-dev "
          "pkg-config libfreetype6-dev libpng12-dev liblapack-dev "
          "libblas-dev gfortran cmake libboost-python-dev liblzma-dev "
          "libjpeg-dev python-virtualenv" % p,
        # install additional dependencies for pip build
        "sudo apt-get %(yes)s install libzbar-dev" % p,
        "sudo apt-get %(yes)s install libimage-exiftool-perl libav-tools" % p,
        # install file-metadata through pip only
        "sudo pip install file-metadata --upgrade",
        # test import of file-metadata
        "python -c'import file_metadata; print(file_metadata.__version__)'",
    ]
    run(ctx, job, yes=yes)


# Test through github
@task
def install_file_metadata_git(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s update" % p,
        # install most recent pip
        # assume pip to be already installed
        "sudo pip install -U pip",
        "pip show pip",
        # install git
        "sudo apt-get %(yes)s install git git-review" % p,
        # install git setup dependencies
        "sudo apt-get %(yes)s install perl openjdk-7-jre python-dev "
          "pkg-config libfreetype6-dev libpng12-dev liblapack-dev "
          "libblas-dev gfortran cmake libboost-python-dev liblzma-dev "
          "libjpeg-dev python-virtualenv" % p,
        # install additional dependencies for pip build
        "sudo apt-get %(yes)s install libzbar-dev" % p,
        "sudo apt-get %(yes)s install libimage-exiftool-perl libav-tools" % p,
        # install file-metadata through git+pip
        "git clone https://github.com/pywikibot-catfiles/file-metadata.git",
        "sudo pip install ./file-metadata --upgrade",
        "sudo pip install -e ./file-metadata",
        # test import of file-metadata
        "python -c'import file_metadata; print(file_metadata.__version__)'",
        # unit-test of file-metadata
        "sudo pip install -r ./file-metadata/test-requirements.txt",
#        "sudo apt-get %(yes)s install python-opencv" % p,  # (opencv-data ?)
        "sudo apt-get %(yes)s install python-opencv opencv-data" % p,
        "cd file-metadata/ && python -m pytest --cov",
    ]
    run(ctx, job, yes=yes)


# Installation of pywikibot
@task
def install_pywikibot(ctx, yes=False):
    p = params(yes=yes)
    job = [
        # install git
        "sudo apt-get %(yes)s install git git-review" % p,
        # install pywikibot
        #"git clone --branch 2.0 --recursive "
        #  "https://gerrit.wikimedia.org/r/pywikibot/core.git",
        "wikibot-filemeta-log || true",
        "sudo pip install "
          "git+https://gerrit.wikimedia.org/r/pywikibot/core.git\#egg="
          "pywikibot",
    ]
    run(ctx, job, yes=yes)


# Install Docker container
@task
def install_docker(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s update" % p,
        "sudo apt-get %(yes)s upgrade" % p,
        "sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys "
          "58118E89F3A912897C070ADBF76221572C52609D" % p,
        "echo \"deb https://apt.dockerproject.org/repo ubuntu-trusty main\" | "
          "sudo tee /etc/apt/sources.list.d/docker.list" % p,
        "sudo apt-get %(yes)s update" % p,
        "sudo apt-get %(yes)s install docker-engine" % p,
        #"sudo service docker start" % p,
    ]
    run(ctx, job, yes=yes)


# Test of pywikibot-catfiles scripts (and file-metadata) including analysis
@task
def test_script(ctx, yes=False, git=False):
    p = params(yes=yes)
    job = [
        "type wikibot-filemeta-log",
        "type wikibot-filemeta-simple",

#        "sudo apt-get %(yes)s install python-opencv" % p,  # (opencv-data ?)
        "sudo apt-get %(yes)s install python-opencv opencv-data" % p,
        # configuration of pywikibot
        #"cd core/ && python pwb.py basic",  # issue: ctx.run stops after this
        #"cd file-metadata/file_metadata/wikibot/ && \"
        #  "python generate_user_files.py",
#        "wikibot-create-config",
# work-a-round hacky login.py replacement: #
        "wget https://raw.githubusercontent.com/drtrigon/catimages-gsoc/"
          "master/user-config.py",
        "wget https://raw.githubusercontent.com/drtrigon/catimages-gsoc/"
          "master/pywikibot.lwp.hack",
        "wget https://raw.githubusercontent.com/drtrigon/catimages-gsoc/"
          "master/login-hack.py",
        "python login-hack.py $PYWIKIBOT_TOKEN",
# end of work-a-round ######################
        "python pwb.py login.py || true",  # (somehow expected to fail)
# download ^^^ from pywikibot scripts directory?
        # run bot tests
        "wikibot-filemeta-log -search:'eth-bib' -limit:5 -logname:test "
          "-dry || true",

        #"cd core/ && python bulk_bot.py "
        #  "-search:'eth-bib' -limit:5 -logname:test -dryrun:1",
        "wikibot-filemeta-log "
          "-search:'eth-bib' -limit:5 -dry",
        "sudo pip install line_profiler memory_profiler",
        "sudo apt-get %(yes)s install valgrind" % p,
        "python -m cProfile -s time wikibot-filemeta-log "
          "-search:'eth-bib' -limit:5 -dry > profile.out && "
          "head profile.out -n 150",
        "kernprof -l -v wikibot-filemeta-log "
          "-search:'eth-bib' -limit:5 -dry && "
          "python -m line_profiler wikibot-filemeta-log.lprof ",
        "python -m memory_profiler wikibot-filemeta-log "
          "-search:'eth-bib' -limit:5 -dry",
        "valgrind --tool=massif --massif-out-file=massif.out "
          "--log-file=valgrind.log wikibot-filemeta-log "
          "-search:'eth-bib' -limit:5 -dry || "  # ignore error
          "cat valgrind.log && ms_print massif.out "
          "|| true",                                      # ignore error
        #"cd core/ && heaptrack python wikibot-filemeta-log "
        #  "-search:'eth-bib' -limit:5 -dry",

        "wikibot-filemeta-simple -cat:SVG_files -limit:5",
    ]
    run(ctx, job, yes=yes)


# Test of THIS invoke script
@task
def test_this(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s install python-flake8" % p,
        #"flake8 tasks.py login-hack.py",
        "flake8 --ignore=E121,E122,E128 tasks.py login-hack.py",
    ]
    run(ctx, job, yes=yes)
