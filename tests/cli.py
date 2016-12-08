#!/usr/bin/python
import base64
import click
import requests


@click.group(chain=True)
def cli():
    pass


@cli.command()
@click.option('--url', default='http://137.138.6.126:32202/fibonacci',
              help='API endpoint')
@click.option('-w', '--weight', default='slow', help='Docker image')
@click.option('-e', '--experiment', default='alice',
              type=click.Choice(['alice', 'atlas', 'cms', 'lhcb', 'recast']),
              help='Experiment to address the request to')
@click.option('-f', '--filename', type=click.Path(exists=True),
              help='Docker image input file')
@click.option('-n', default='1',
              type=click.IntRange(min=1, max=40),
              help='Number of requests')
def fibonacci(url, weight, experiment, filename, n):
    with open(click.format_filename(filename)) as f:
        input_file = f.read()

    input_file_b64 = base64.encodestring(input_file.encode())

    data = {
        'weight': weight,
        'experiment': experiment,
        'input-file': input_file_b64
    }

    for i in range(n):
        response = requests.post(url, json=data)
        click.echo('Request {} of {}: {}'.format(i+1, n, response.text))


import yaml
def getinit_data(initfiles, parameters):
    '''
    get initial data from both a list of files and a list of 'pname=pvalue'
    strings as they are passed in the command line <pvalue> is assumed to be a
    YAML parsable string.
    '''
    initdata = {}
    for initfile in initfiles:
        initdata.update(**yaml.load(open(initfile)))

    for x in parameters:
        key, value = x.split('=')
        initdata[key] = yaml.load(value)
    return initdata


@cli.command()
@click.option('--url', default='http://137.138.6.126:32202/yadage',
              help='API endpoint')
@click.option('-e', '--experiment', default='alice',
              type=click.Choice(['alice', 'atlas', 'cms', 'lhcb', 'recast']),
              help='Experiment to address the request to')
@click.option('-t', '--toplevel', default='toplevel', help='Toplevel')
@click.option('-w', '--workflow', default='workflow', help='Yadage Workflow')
@click.option('-a','--archive', default = None)
@click.option('--parameter', '-p', multiple=True)
def yadage(url, experiment, toplevel, workflow, parameter, archive):
    initdata = getinit_data([],parameter)
    click.echo('initdata: %s' % initdata)

    data = {
        'experiment': experiment,
        'toplevel': toplevel,
        'workflow': workflow,
        'parameters': initdata,
    }
    if archive:
        data.update(inputarchive = archive)
    response = requests.post(url, json=data)
    click.echo('Request Response: {}'.format(response.text))

if __name__ == '__main__':
    cli()
