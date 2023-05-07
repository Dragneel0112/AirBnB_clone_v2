#!/usr/bin/python3
"""
Compresses folder web static
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Function to compress directory web static
        Return: path to archive on success; None on fail
    """
    # Obtain date and time
    now = datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    archive_path = "versions/web_static_{}.tgz".format(now)

    # Create versions directory and archive
    local('mkdir -p versions/')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # If sucess return path else NONE
    if result.succeeded:
        return archive_path
    return None
