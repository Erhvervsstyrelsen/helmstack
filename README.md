# Helmstack

Helmstack is heavily inspired by [helmfile](https://github.com/roboll/helmfile).

helmfile is a great project and way more advanced than helmstack. But I found it difficult to use when dealing with multiple chart versions spanning different environments.

The idea behind helmstack is that you have a basic stack file for which you use overlays to handle different versions in different environments. Thus making it easy to deal with having one version in dev, another in test and disabling the same chart in prod.

## Install
```bash
pip install helmstack
```

## Development setup
```bash
virtualenv venv
source venv/bin/activate
pip install --editable .
```

## Stack file example

Default stack file is `stackfile.yaml`
```yaml
releases:
  - name: web-env
    namespace: web
    chart: chart/web-env

  - name: web-app
    namespace: web
    chart: chart/web-app

environments: # Optional
  dev:
    overlay:
      - env/dev.yaml
  prod:
    overlay:
      - env/prod.yaml

repositories: # Optional
  - name: chart
    url: https://chartmuseum.somewhere.dk

helmDefaults: # Optional
  recreatePods: true
  force: true
```

## Overlay example (env/dev.yaml)
```yaml
releases:
  web-env:
    version: 1.7.0
    enabled: true
  web-app:
    version: 1.39.0
    enabled: true
```

## Release
```bash
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## TODO

### Write tests
So far this is a POC but tests should be written

### Skip repo's
Add flag --skip-repos

### Templating
Support some sort of templating language... Maybe

### s/overlay/overlays/ ?
Either stop supporting multiple overlay files or rename key to overlays
