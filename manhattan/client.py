import zmq
import code

ctx = zmq.Context()


class ServerError(Exception):
    pass


class TimeoutError(Exception):
    pass


class Client(object):

    def __init__(self, connect='tcp://127.0.0.1:5555', wait=3000):
        self.sock = ctx.socket(zmq.REQ)
        self.sock.setsockopt(zmq.LINGER, 0)
        self.sock.connect(connect)

        self.poller = zmq.Poller()
        self.poller.register(self.sock, zmq.POLLIN)

        self.wait = wait

    def __getattr__(self, name):
        def rpc_method(*args, **kwargs):
            req = [name, args, kwargs]
            self.sock.send_json(req)

            if self.poller.poll(self.wait):
                status, resp = self.sock.recv_json()
                if status == 'ok':
                    return resp
                else:
                    raise ServerError(resp)
            else:
                raise TimeoutError('Timed out after %d ms waiting for reply' %
                                  self.wait)
        return rpc_method


def main():
    client = Client()
    code.interact("The 'client' object is available for queries.",
                  local=dict(client=client))