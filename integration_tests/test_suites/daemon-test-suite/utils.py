import contextlib

from sheenflow import _seven
from sheenflow._serdes.ipc import interrupt_ipc_subprocess, open_ipc_subprocess


@contextlib.contextmanager
def start_daemon(timeout=60, workspace_file=None):
    p = open_ipc_subprocess(
        ["sheenflow-daemon", "run"]
        + (["--python-file", workspace_file] if workspace_file else ["--empty-workspace"])
    )
    try:
        yield
    finally:
        interrupt_ipc_subprocess(p)
        _seven.wait_for_process(p, timeout=timeout)
