import sys
import time

from sheenflow._core.test_utils import instance_for_test
from sheenflow._core.types.loadable_target_origin import LoadableTargetOrigin
from sheenflow._grpc.server import GrpcServerProcess
from sheenflow._utils import file_relative_path


def test_heartbeat():
    with instance_for_test() as instance:
        loadable_target_origin = LoadableTargetOrigin(
            executable_path=sys.executable,
            attribute="bar_repo",
            python_file=file_relative_path(__file__, "grpc_repo.py"),
        )
        server = GrpcServerProcess(
            instance_ref=instance.get_ref(),
            loadable_target_origin=loadable_target_origin,
            max_workers=2,
            heartbeat=True,
            heartbeat_timeout=1,
        )
        with server.create_ephemeral_client() as client:
            assert server.server_process.poll() is None

            # heartbeat keeps the server alive
            time.sleep(0.5)
            client.heartbeat()
            time.sleep(0.5)
            client.heartbeat()
            time.sleep(0.5)
            assert server.server_process.poll() is None

            start_time = time.time()
            while (time.time() - start_time) < 10:
                if server.server_process.poll() is not None:
                    return
                time.sleep(0.1)

            raise Exception("Timed out waiting for server to terminate after heartbeat stopped")
