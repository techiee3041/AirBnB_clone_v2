#!/usr/bin/python3
""" web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

# Define variables
env.hosts = ["100.25.200.118", "54.237.88.4"]
archive_destination = "versions"
archive_name_format = "web_static_{year}{month}{day}{hour}{minute}{second}.tgz"

@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir(archive_destination):
        os.mkdir(archive_destination)
    cur_time = datetime.now()
    archive_name = archive_name_format.format(
        year=cur_time.year,
        month=cur_time.month,
        day=cur_time.day,
        hour=cur_time.hour,
        minute=cur_time.minute,
        second=cur_time.second
    )
    archive_path = os.path.join(archive_destination, archive_name)
    try:
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))
        archive_size = os.stat(archive_path).st_size
        print("web_static packed: {} -> {} Bytes".format(archive_path, archive_size))
    except Exception:
        archive_path = None
    return archive_path

def do_deploy(archive_path):
    """Deploys the static files to the host servers.
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success

