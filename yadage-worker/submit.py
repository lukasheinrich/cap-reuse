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
    return job_id

def check_status(job_id):
    response = requests.get(
        'http://{host}/{api}/{resource}/{id}'.format(
            host='step-broker-service.default.svc.cluster.local',
            api=API_VERSION,
            resource='jobs',
            id=job_id
        ),
        headers = {'cache-control':'no-cache'}
    )

    job_info = response.json()['job']
    log.info('job information: %s',job_info)
    return job_info
