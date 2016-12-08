from packtivity.handlers.environment_handlers import environment

import logging
from submit import submit
import pipes

log = logging.getLogger('yadage.cap')

@environment('docker-encapsulated','cap')
def run_in_env(environment,context,job):
    log.info('running an job for CAP. Turnaround!!')
    log.info('job is %s',job)

    command = job['command']
    image   = environment['image']
    tag     = environment['imagetag']


    log.info('state context is %s',context)
    log.info('would run (%s) in %s:%s',command,image,tag)

    log.info('submitting!')

    wrapped_cmd = 'sh -c {}  '.format(
        pipes.quote(command)
    )

    submit('atlas', image, wrapped_cmd)
