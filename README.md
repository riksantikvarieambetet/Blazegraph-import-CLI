# Blazegraph import CLI

Command line interface for importing RDF files to Blazegraph from the client file system or a list of URLs.

## Prerequirements

 - GIT
 - Python 3.6
 - [pipenv](https://docs.pipenv.org/)

## Installing

```bash
git clone https://github.com/riksantikvarieambetet/Blazegraph-import-CLI.git
cd Blazegraph-import-CLI
pipenv install
```

## Usage Examples

*Heads up: This program might use all the systems available CPUs.*

**Import from a directory containing RDF files**

```bash
pipenv run python import.py --endpoint=http://172.17.0.1:9999/blazegraph/ --namespace=kb --rdfs=/path/to/dir
```

**Import from a list of URLs**

The target file should have its URLs separated by line breaks.

```bash
pipenv run python import.py --endpoint=http://172.17.0.1:9999/blazegraph/ --namespace=kb --urls=/path/to/file.txt
```

**Help**

```bash
pipenv run python import.py --help
```
