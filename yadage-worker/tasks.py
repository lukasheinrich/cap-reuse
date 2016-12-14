from __future__ import absolute_import

from __future__ import print_function
from worker.celery import app
from worker.submit import submit
import os
import pipes

import logging
import yaml
import subprocess
import shlex
import time
import json
log = logging.getLogger(__name__)

API_VERSION = 'api/v1.0'


@app.task(name='tasks.run_yadage_workflow', ignore_result=True)
def run_yadage_workflow(ctx):
    log.info('Hello This is Lukas Talking... testing the turnaround time')

    log.info('running recast workflow on context: {ctx}'.format(
            ctx = ctx
        )
    )

    jobguid = run_yadage_workflow.request.id

    taskdir = os.path.join('/data',jobguid)

    if not os.path.exists(taskdir):
        os.makedirs(taskdir)

    workdir = os.path.join(taskdir,'yadage')


    #here we consider parameters passed to the task as presets while parameters
    #passed in a potential initial archive would be considered instance-specific


    presetfilename = os.path.join(taskdir,'_preset.yaml')
    with open(presetfilename,'w') as presetfile:
        yaml.dump(ctx['preset_pars'],presetfile, default_flow_style = False)

    yadage_env = os.environ.copy()

    yadage_env['YADAGE_PACKIMPORT'] = 'worker.cappack'
    yadage_env['YADAGE_PACKCONFIG'] = json.dumps({
        'environment':{
            'docker-encapsulated': 'cap'
        }
    })



    input_option = '-a {}'.format(ctx['inputarchive']) if 'inputarchive' in ctx else ''

    cmd = 'yadage-run -u {updateinterval} -b {backend} -t {toplevel} {workdir} {workflow} {presetpar} {input_option}'.format(
        updateinterval = 3,
        backend = 'multiproc:{}'.format(ctx.get('nparallel',10)),
        toplevel = ctx['toplevel'],
        workdir = workdir,
        workflow = ctx['workflow'],
        presetpar = presetfilename,
        input_option = input_option
    )

    log.info('running cmd: %s',cmd)

    proc = subprocess.Popen(shlex.split(cmd),
                            env = yadage_env,
                            stderr = subprocess.STDOUT,
                            stdout = subprocess.PIPE)



    filelogger = logging.getLogger('yadage_output')
    filelogger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('{}/fullyadage.log'.format(taskdir))
    fh.setLevel(logging.DEBUG)
    filelogger.addHandler(fh)
    filelogger.propagate = False

    while True:
        s = proc.stdout.readline().strip()
        if s:
            filelogger.debug(s)
            try:
                splitup = s.split(':',1)
                if len(splitup)==2:
                    level,rest = splitup
                    thelevel = getattr(logging,level)
                    for line in rest.splitlines():
                        if 'adage' in line or thelevel>logging.INFO:
                            log.log(thelevel,rest)
            except AttributeError:
                pass
        else:
            if proc.poll() is not None:
                break
        time.sleep(0.01)
        
    log.info('workflow process terminated task')
    if proc.returncode:
        log.error('workflow failed, raising error')
        raise RuntimeError('failed workflow process return code {}'.format(proc.returncode))
