FROM cern/cc7-base
RUN yum install -y gcc gcc-c++ graphviz-devel ImageMagick python-devel libffi-devel openssl openssl-devel unzip nano autoconf automake libtool
RUN curl https://bootstrap.pypa.io/get-pip.py | python -
RUN echo what 6
RUN pip install celery==3.1.17
RUN pip install https://github.com/diana-hep/packtivity/archive/master.zip
RUN pip install https://github.com/diana-hep/yadage/archive/master.zip
RUN pip install zmq python-socketio gevent flask gevent-websocket
ADD . /code
WORKDIR /code
