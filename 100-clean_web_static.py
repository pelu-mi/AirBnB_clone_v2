#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers
    using the function deploy and clean using do_clean
"""

from fabric.api import sudo, local
from fabric.context_managers import cd, lcd

env.hosts = ['3.94.211.137', '54.237.207.59']


def do_clean(number=0):
    """ Clean up and delete out-of-date archives from the local directory
        and the web server
    """
    if number < 1:
        number = 1
    # Clean locally
    with lcd('versions'):
        local('e=$( ls -t | wc -l ); while [ $e -gt {} ]; \
do f=$( ls -t | tail -1 ); sudo rm $f; e=$(( $e - 1 )); done').format(number)
    # Clean server
    with cd('/data/web_static/releases'):
        sudo('e=$( ls -t | wc -l ); while [ $e -gt {} ]; \
do f=$( ls -t | tail -1 ); rm -r $f; e=$(( $e - 1 )); done').format(number)
