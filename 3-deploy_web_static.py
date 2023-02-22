#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers
    using the function deploy
"""

from fabric.api import env, put, sudo, local
from datetime import datetime
from os import path


env.hosts = ['3.94.211.137', '54.237.207.59']


def do_pack():
    """ Generate a .tgz archive from the contents of the web_static folder
    """
    try:
        local('mkdir -p versions')
        now = datetime.now()
        name = "versions/web_static_" + now.strftime("%Y%m%d%H%M%S") + '.tgz'
        local('tar -czvf ' + name + ' web_static')
        return name
    except Exception as e:
        return None


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
        web_foldr = '/data/web_static/releases/'
        # Commands
        sudo('mkdir -p {}{}'.format(web_foldr, folder))
        sudo('tar -zxvf /tmp/{0}.tgz -C {1}{0}'.format(folder, web_foldr))
        sudo('mv {0}{1}/web_static/* {0}{1}/'.format(web_foldr, folder))
        # Delete unneeded files
        sudo('rm /tmp/{}.tgz'.format(folder))
        sudo('rm -rf {0}{1}/web_static'.format(web_foldr, folder))
        sudo('rm ' + current)
        # Create symbolic link to web_static folder
        sudo('ln -s {}{} {}'.format(web_foldr, folder, current))
        return True
    except Exception as e:
        return False


def deploy():
    """ Combine do_pack and do_deploy
    """
    archive_name = do_pack()
    return do_deploy(archive_name)
