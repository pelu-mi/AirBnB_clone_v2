#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers
    using the function deploy and clean using do_clean
"""

from fabric.api import sudo, local, env
from fabric.context_managers import cd, lcd

env.hosts = ['3.94.211.137', '54.237.207.59']


def do_clean(number=0):
    """ Clean up and delete out-of-date archives from the local directory
        and the web server
    """
    num = 1 if int(number) < 1 else int(number)
    # Clean locally
    archives = sorted(os.listdir('versions/'))
    for i in range(num):
        archives.pop()
    with lcd('versions/'):
        for archive in archives:
            local('rm ./{}'.format(archive))
    # Clean server
    with cd("/data/web_static/releases"):
        archives = run('ls -tr').split()
        archives = [arch for arch in archives if 'web_static_' in arch]
        for i in range(num):
            archives.pop()
        for archive in archives:
            sudo('rm -rf ./{}'.format(archive))
