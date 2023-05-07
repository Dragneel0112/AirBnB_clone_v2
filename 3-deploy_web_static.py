#!/usr/bin/python3
'''
Using fab to deploy .tgz archive from the contents
of the web_static to remote server
'''
from fabric.api import local, env, put, run
import os
import time

env.user = 'ubuntu'
env.hosts = ['54.237.108.151', '100.25.111.49']
env.key_filename = '~/.ssh/school'


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


def do_deploy(archive_path):
    '''
    Deploys an archive to remote webservers
    '''
    if not os.path.isfile(archive_path):
        return False

    # Upload the archive to /tmp/ directory in server
    put(archive_path, '/tmp/')

    # Create location to extract the files
    file_name = archive_path.split('/')[-1]  # Gets file name
    dir_path = '/data/web_static/releases/{}'.format(file_name.split('.')[0])
    run('mkdir -p {}'.format(dir_path))

    # Uncompress the archive to the folder
    server_archive_path = '/tmp/' + file_name  # Path of archive in server
    run('tar -xzf {} -C {}'.format(server_archive_path, dir_path))

    # Delete the archive from the web server
    run('rm -rf {}'.format(server_archive_path))

    # Delete the symbolic link
    run('rm -rf /data/web_static/current')

    # Move the files from web_static to web_static_<number>
    run('mv {}/web_static/* {}'.format(dir_path, dir_path))
    run('rm -rf {}/web_static'.format(dir_path))

    # Create a new symbolic link
    run('ln -s {} /data/web_static/current'.format(dir_path))

    return True


def deploy():
    """
    Using do_pack and do_deploy to deply files to server
    """
    return do_deploy(do_pack())
