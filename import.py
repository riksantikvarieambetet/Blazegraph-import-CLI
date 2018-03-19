import glob
import time

import click
import requests

import background

headers = {
    'Content-Type': 'application/rdf+xml',
}

count = 0

def error(text):
    click.secho(text, err=True, fg='red')
    exit()

def import_from_uri(uri, sparql_endpoint):
    pass

def confirm_import_from_uris(data, sparql_endpoint):
    pass

@background.task
def import_from_file(filepath, sparql_endpoint):
    global count
    rdf = None
    with open(filepath, 'r', encoding='utf-8') as f:
        rdf = f.read()

    r = requests.post(sparql_endpoint, data=rdf.encode('utf-8'), headers=headers)
    click.secho('Importing: {0} | '.format(filepath), fg='yellow', nl=False)
    if not 'modified' in r.text or r.status_code is not 200:
        click.secho('Failed', fg='red')
    else:
        click.secho('Success', fg='green')

    count += 1

def confirm_imports_from_dir(path, sparql_endpoint):
    files = glob.glob(path + '/*.rdf')

    click.secho('Found {0} RDF files.'.format(len(files)), fg='green')
    click.echo('This program might use all the systems available CPUs({0})!'.format(background.n))
    click.echo('Would you like to proceed with the download? y/n')

    c = click.getchar()
    if c == 'y':
        for f in files:
            import_from_file(f, sparql_endpoint)

        # the sleep is used for performance reasons
        while count < len(files):
            time.sleep(0.5)

        click.secho('Done!', fg='green')
    exit()

@click.command()
@click.option('--endpoint', default='http://172.17.0.1:9999/blazegraph/', help='The endpoint of your Blazegraph instance.')
@click.option('--namespace', default='kb', help='The Blazegraph namespace you want to import into.')
@click.option('--rdfs', type=click.Path(exists=True), help='The path to your RDF files.')
@click.option('--uris', type=click.File('r'), help='The path to your list of URIs.')
def start(endpoint, namespace, rdfs=False, uris=False):
    click.secho('Validating given arguments...', fg='yellow')

    data = None
    if rdfs:
        if not glob.glob(rdfs + '/*.rdf'):
            error('The given directory contains no RDF files:\n{0}'.format(rdfs))
    elif uris:
        click.echo(uris)
        data = uris.read()
        uris.close()
    else:
        error('"rdfs" and "uris" arguments are both missing. One of them should allways be defined.')

    sparql_endpoint = '{0}namespace/{1}/sparql'.format(endpoint, namespace)
    r = requests.head(sparql_endpoint)
    if r.status_code is not 200 and 'application/xml' not in r.headers['Content-Type']:
        error('Failed to validate SparQL endpoint:\n{0}'.format(sparql_endpoint))

    if data:
        confirm_import_from_uris(data, sparql_endpoint)
    else:
        confirm_imports_from_dir(rdfs, sparql_endpoint)

if __name__ == '__main__':
    start()
