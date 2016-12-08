API_VERSION = 'api/v1.0'
import requests
import json
import logging
log = logging.getLogger('yadage.cap.submit')

def submit(experiment, image, cmd):
    job_spec = {
        'experiment': experiment,
        'docker-img': image,
        'cmd': cmd,
        'env-vars': {}
    }

    log.info('submitting %s',json.dumps(job_spec, indent = 4, sort_keys = True))

    response = requests.post(
        'http://{host}/{api}/{resource}'.format(
            host='step-broker-service.default.svc.cluster.local',
            api=API_VERSION,
            resource='jobs'
        ),
        json=job_spec,
        headers={'content-type': 'application/json'}
    )

    job_id = str(response.json()['job-id'])
    log.info('Job {} sucessfully created'.format(job_id))

    log.info('will block until we are done!')

    #block until job is done...
    while True:
        response = requests.get(
        'http://{host}/{api}/{resource}/{id}'.format(
            host='step-broker-service.default.svc.cluster.local',
            api=API_VERSION,
            resource='jobs',
            id=job_id))

        job_info = response.json()['job']
        print('job information: {}'.format(job_info))
        if job_info['status'] != 'started':
            break
        import time
        log.info('job is still in started mode.. sleep for 10 seconds')
        time.sleep(10)
    log.info('Job finished with info: {}'.format(job_info))
