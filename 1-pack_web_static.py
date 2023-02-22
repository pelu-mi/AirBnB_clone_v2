#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the
    web_static folder of the AirBnB Clone repo, using the function do_pack
"""

from fabric.api import local
from datetime import datetime


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
