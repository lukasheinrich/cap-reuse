import zmq
ctx = zmq.Context()


backend  = ctx.socket(zmq.XSUB)
backend.bind('tcp://*:8666')

frontend  = ctx.socket(zmq.XPUB)
frontend.bind('tcp://*:8667')

proxy = zmq.proxy(frontend, backend)
