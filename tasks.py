#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hi There!
# This script serves for the purpose of installing a testing environment to a
# Kubuntu VirtualBox guest as described in User:DrTrigon/file-metadata:
# https://commons.wikimedia.org/wiki/User:DrTrigon/file-metadata
#
# Usage:
# $ invoke install_file_metadata_spm install_pywikibot \
#     install_file_metadata_bot
# $ invoke install_file_metadata_pip install_pywikibot \
#     install_file_metadata_bot
# $ invoke install_pywikibot install_file_metadata_git \
#     (install_file_metadata_bot)
# $ invoke install_pywikibot --yes install_file_metadata_git --yes
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
    install_pip(ctx, yes=yes)
    install_file_metadata_deps_spm(ctx, yes=yes)
    install_file_metadata(ctx, yes=yes)


def install_pip(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s update" % p,
        "sudo apt-get %(yes)s purge python-pip && "
          "sudo apt-get %(yes)s autoremove" % p,
        "wget https://bootstrap.pypa.io/get-pip.py && sudo python get-pip.py",
        "pip show pip",
    ]
    run(ctx, job, yes=yes)


def install_file_metadata_deps_spm(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s install python-appdirs python-magic "
          "python-numpy python-scipy python-matplotlib python-wand "
          "python-skimage python-zbar cmake libboost-python-dev "
          "liblzma-dev libjpeg-dev libz-dev" % p,
    ]
    run(ctx, job, yes=yes)


def install_file_metadata(ctx, yes=False):
    p = params(yes=yes)
    job = [
        #"sudo pip install file-metadata --upgrade",
        # work-a-round since above commands only installs 0.1.0 not dev! #
        # file-metadata-0.1.0 was installed as:
        # /usr/local/lib/python2.7/dist-packages/file_metadata/VERSION
        "sudo apt-get %(yes)s install libimage-exiftool-perl "
          "libmagickwand-dev libav-tools libzbar-dev" % p,
        "sudo git clone https://github.com/pywikibot-catfiles/"
          "file-metadata.git /usr/local/lib/python2.7/dist-packages/"
          "file-metadata",
        "sudo pip install /usr/local/lib/python2.7/dist-packages/"
          "file-metadata/ --upgrade",
        # end of work-a-round ############################################
        "python -c'import file_metadata; print(file_metadata.__version__)'",
    ]
    run(ctx, job, yes=yes)


# Test through pip
@task
def install_file_metadata_pip(ctx, yes=False):
    install_pip(ctx, yes=yes)
    install_file_metadata_deps_pip(ctx, yes=yes)
    install_file_metadata(ctx, yes=yes)


def install_file_metadata_deps_pip(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s install perl openjdk-7-jre python-dev "
          "pkg-config libfreetype6-dev libpng12-dev liblapack-dev "
          "libblas-dev gfortran cmake libboost-python-dev liblzma-dev "
          "libjpeg-dev python-virtualenv" % p,
    ]
    run(ctx, job, yes=yes)


# Test through github
@task
def install_file_metadata_git(ctx, yes=False):
    install_pip(ctx, yes=yes)
    install_file_metadata_deps_pip(ctx, yes=yes)
    p = params(yes=yes)
    job = [
        "git clone https://github.com/AbdealiJK/file-metadata.git",
        "sudo apt-get %(yes)s install libzbar-dev" % p,
        "sudo apt-get %(yes)s install libimage-exiftool-perl libav-tools" % p,
        "cd file-metadata/ && sudo pip install . --upgrade",
        "cd file-metadata/ && python -c'import file_metadata; "
          "print(file_metadata.__version__)'",
        "cd core/ && ln -s ../file-metadata/file_metadata file_metadata",
    ]
    run(ctx, job, yes=yes)


# Installation of pywikibot
@task
def install_pywikibot(ctx, yes=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s update" % p,
        "sudo apt-get %(yes)s install git git-review" % p,
        "git clone --branch 2.0 --recursive "
          "https://gerrit.wikimedia.org/r/pywikibot/core.git",
    ]
    run(ctx, job, yes=yes)
    configure_pywikibot(ctx, yes=yes)


# Test bot script
@task
def install_file_metadata_bot(ctx, yes=False):
    job = [
#        "sudo apt-get %(yes)s install libmagickwand-dev" % p,
        "cd core/ && wget https://raw.githubusercontent.com/"
          "pywikibot-catfiles/file-metadata/master/file_metadata/"
          "wikibot/simple_bot.py",
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
    configure_docker(ctx, yes=yes)


# Configuration of pywikibot
@task
def configure_pywikibot(ctx, yes=False):
    job = [
        #"cd core/ && python pwb.py basic",  # issue: ctx.run stops after this
        "cd core/ && wget https://raw.githubusercontent.com/drtrigon/"
          "catimages-gsoc/master/user-config.py",
    ]
    run(ctx, job, yes=yes)


# Configuration of docker for running tests
@task
def configure_docker(ctx, yes=False):
    job = [
        "sudo docker pull drtrigon/catimages-gsoc",
    ]
    run(ctx, job, yes=yes)


# Test of pywikibot-catfiles scripts (and file-metadata) including analysis
@task
def test_script(ctx, yes=False, git=False):
    p = params(yes=yes)
    job = [
        "sudo apt-get %(yes)s install python-opencv" % p,
    ]
    run(ctx, job, yes=yes)
    test_script_simple_bot(ctx, yes=yes, git=git)
    test_script_bulk(ctx, yes=yes, git=git)


def test_script_simple_bot(ctx, yes=False, git=False):
    if not git:
        job = [
            "cd core/ && python pwb.py simple_bot.py -cat:SVG_files -limit:5",
    ]
    else:
        job = [
            "cd core/ && python pwb.py file_metadata/wikibot/simple_bot.py "
              "-cat:SVG_files -limit:5",
    ]
    run(ctx, job, yes=yes)


def test_script_bulk(ctx, yes=False, git=False):
    p = params(yes=yes)
    job = [
        "cd core/ && wget https://raw.githubusercontent.com/"
          "pywikibot-catfiles/file-metadata/ajk/work/file_metadata/"
          "wikibot/bulk_bot.py",
# work-a-round hacky login.py replacement: #
        "cd core/ && wget https://raw.githubusercontent.com/drtrigon/"
          "catimages-gsoc/master/pywikibot.lwp.hack",
        "cd core/ && wget https://raw.githubusercontent.com/drtrigon/"
          "catimages-gsoc/master/login-hack.py",
        "cd core/ && python login-hack.py $PYWIKIBOT_TOKEN",
# end of work-a-round ######################
        "cd core/ && python pwb.py login.py",
        #"cd core/ && python bulk_bot.py "
        #  "-search:'eth-bib' -limit:5 -logname:test -dryrun:1",
        "cd core/ && python bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry",
        "sudo pip install line_profiler memory_profiler",
        "sudo apt-get %(yes)s install valgrind" % p,
        "cd core/ && python -m cProfile -s time bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry > profile.out && "
          "head profile.out -n 150",
        "cd core/ && kernprof -l -v bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry && "
          "python -m line_profiler bulk_bot.py.lprof ",
        "cd core/ && python -m memory_profiler bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry",
        "cd core/ && valgrind --tool=massif --massif-out-file=massif.out "
          "--log-file=valgrind.log python bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry || "  # ignore error
          "cat valgrind.log && ms_print massif.out "
          "|| true",                                      # ignore error
        #"cd core/ && heaptrack python bulk_bot.py "
        #  "-search:'eth-bib' -limit:5 -dry",
    ]
    run(ctx, job, yes=yes)


# Test of docker image contained scripts
@task
def test_docker(ctx, yes=False):
    p = params(yes=yes)
#    p['travis'] = '-i' if travis else '-it'
    p['travis'] = '-i'  # use -i instead of -it due to tty
    job = [
        "sudo docker run %(travis)s drtrigon/catimages-gsoc "
          "bash -c \"cd /opt/pywikibot-core && python pwb.py "
          "../file-metadata/file_metadata/wikibot/simple_bot.py "
          "-cat:SVG_files -limit:5 && cd /\"" % p,
# work-a-round hacky login.py replacement: #
# !!!ISSUE: make 'login.py -pass:xxx' work or use -oauth token
# !!!TODO: need a way to run bulk_bot.py w/o needing to enter a passwd,
#          e.g. like -simulate
        #"sudo docker run %(travis)s drtrigon/catimages-gsoc "
        #  "bash -c \"python bulk.py -search:'eth-bib' "
        #  "-limit:5 -logname:test -dryrun:1 "
        #  "-dir:/opt/pywikibot-core/\"" % p,
        "sudo docker run %(travis)s drtrigon/catimages-gsoc "
          "bash -c \"cd /opt/pywikibot-core && "
          "python login-hack.py $PYWIKIBOT_TOKEN && "
          "cd /opt/pywikibot-core && "
          "python pwb.py login.py\"" % p,  # check login
        "sudo docker run %(travis)s drtrigon/catimages-gsoc "
          "bash -c \"cd /opt/pywikibot-core && "
          "python login-hack.py $PYWIKIBOT_TOKEN && "
          "cd / && python bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry "
          "-dir:/opt/pywikibot-core/\"" % p,
#        "sudo docker run %(travis)s drtrigon/catimages-gsoc "
#          "bash -c \"cd /opt/pywikibot-core && "
#          "python pwb.py /bulk_bot.py "
#          "-search:'eth-bib' -limit:5 -dry "
#          "-dir:/opt/pywikibot-core/\"" % p,
        "sudo docker run %(travis)s drtrigon/catimages-gsoc "
          "bash -c \"cd /opt/pywikibot-core && "
          "python login-hack.py $PYWIKIBOT_TOKEN && "
          "cd / && python -m cProfile -s time bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry "
          "-dir:/opt/pywikibot-core/ > profile.out && "
          "head profile.out -n 150\"" % p,
        "sudo docker run %(travis)s drtrigon/catimages-gsoc "
          "bash -c \"cd /opt/pywikibot-core && "
          "python login-hack.py $PYWIKIBOT_TOKEN && "
          "cd / && sudo apt-get %(yes)s install valgrind && "
          "valgrind --tool=massif --massif-out-file=massif.out "
          "--log-file=valgrind.log python bulk_bot.py "
          "-search:'eth-bib' -limit:5 -dry "
          "-dir:/opt/pywikibot-core/ && "
          "cat valgrind.log && ms_print massif.out\"" % p,
# end of work-a-round ######################
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
