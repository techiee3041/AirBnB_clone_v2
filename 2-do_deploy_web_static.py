#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run, hosts
from os.path import exists
from datetime import datetime

# Define server information
servers = {
    '253642-web-01': {
        'ip': '100.25.200.118',
        'user': 'ubuntu'
    },
    '253642-web-02': {
        'ip': '54.237.88.4',
        'user': 'ubuntu'
    }
}

# Set the environment variables based on server information
env.hosts = [servers[server]['ip'] for server in servers]
env.user = servers['253642-web-01']['user']  # You can choose any server as a reference

def do_pack():
    """Create a compressed archive of your web_static directory"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static".format(timestamp))
        return "versions/web_static_{}.tgz".format(timestamp)
    except Exception:
        return None

def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        path_no_extension = "/data/web_static/releases/{}".format(archive_name.split('.')[0])
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_extension))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, path_no_extension))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}/".format(path_no_extension, path_no_extension))
        run("rm -rf {}/web_static".format(path_no_extension))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_no_extension))
        return True
    except Exception:
        return False

def deploy():
    """Deploy the web_static content to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)

