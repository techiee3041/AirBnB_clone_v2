#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
import sys
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

# Define default values (in case they are not provided as command-line arguments)
default_host_servers = ["100.25.200.118", "54.237.88.4"]
default_archive_directory = "versions"

# Use command-line arguments if provided, otherwise use default values
host_servers = sys.argv[1:] if len(sys.argv) > 1 else default_host_servers
archive_directory = sys.argv[2] if len(sys.argv) > 2 else default_archive_directory

env.hosts = host_servers
"""The list of host server IP addresses."""


@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir(archive_directory):
        os.mkdir(archive_directory)
    cur_time = datetime.now()
    output = f"{archive_directory}/web_static_{cur_time.strftime('%Y%m%d%H%M%S')}.tgz"
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
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

