#!/usr/bin/python3
"""A web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_t = datetime.now()
    outp = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_t.year,
        cur_t.month,
        cur_t.day,
        cur_t.hour,
        cur_t.minute,
        cur_t.second
    )
    try:
        print("Packing web_static to {}".format(outp))
        local("tar -cvzf {} web_static".format(outp))
        archize_size = os.stat(outp).st_size
        print("web_static packed: {} -> {} Bytes".format(outp, archize_size))
    except Exception:
        outp = None
    return outp
