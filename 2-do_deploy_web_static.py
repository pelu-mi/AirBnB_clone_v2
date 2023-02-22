#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers
    using the function do_deploy
"""

from fabric.api import env, local, run
from datetime import datetime
from os import path


env.hosts = ['3.94.211.137', '54.237.207.59']

def do_deploy(archive_path):
    """ Distributes an archive to the web servers
    """
    try:
        if not path.exists(archive_path):
            return False
        put(archive_path, '/tmp/')
        # Slice string
        folder = archive_path[9:-4]
        current = '/data/web_static/current'
        # Commands
        sudo('mkdir -p /data/web_static/releases/{}'.format(folder))
        sudo('tar -zxvf /tmp/{}.tgz -C \
             /data/web_static/releases/{}'.format(folder, folder))
        sudo('rm /tmp/{}.tgz'.format(folder))
        sudo('rm ' + current)
        sudo('ln -s /data/web_static/releases/{} {}'.format(folder, current))
        return True
    except Exception as e:
        return False
