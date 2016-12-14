FROM cern/cc7-base
RUN yum install -y gcc gcc-c++ graphviz-devel ImageMagick python-devel libffi-devel openssl openssl-devel unzip nano autoconf automake libtool
RUN curl https://bootstrap.pypa.io/get-pip.py | python -
RUN echo what 3
RUN pip install celery==3.1.17
RUN pip install https://github.com/diana-hep/packtivity/archive/master.zip
RUN pip install https://github.com/diana-hep/yadage/archive/master.zip
RUN pip install jupyter
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
ADD . /workdir/worker
WORKDIR /workdir
ARG QUEUE_ENV=default
ENV QUEUE_ENV ${QUEUE_ENV}
ENV PYTHONPATH=/workdir
ENV PACKTIVITY_ASYNCBACKEND worker.externalbackend:ExternalBackend:ExternalProxy
CMD celery -A worker worker -l info -Q ${QUEUE_ENV}

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
ENV TINI_VERSION v0.13.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--NotebookApp.token=''"]
