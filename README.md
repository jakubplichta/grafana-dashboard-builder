# grafana-dashboard-builder

[![PyPI version](https://badge.fury.io/py/grafana-dashboard-builder.svg)](http://badge.fury.io/py/grafana-dashboard-builder) [![Build Status](https://travis-ci.org/jakubplichta/grafana-dashboard-builder.svg?branch=master)](https://travis-ci.org/jakubplichta/grafana-dashboard-builder) [![Coverage Status](https://coveralls.io/repos/jakubplichta/grafana-dashboard-builder/badge.svg?branch=master)](https://coveralls.io/r/jakubplichta/grafana-dashboard-builder?branch=master)

## Introduction

_grafana-dashboard-builder_ is an open-source tool for easier creation of [Grafana](http://grafana.org/) dashboards.
It is written in [Python](https://www.python.org/) and uses [YAML](http://yaml.org/) descriptors for dashboard
templates.

This project has been inspired by [Jenkins Job Builder](https://github.com/openstack-infra/jenkins-job-builder) that
allows users to describe [Jenkins](https://jenkins-ci.org/) jobs with human-readable format. _grafana-dashboard-builder_
aims to provide similar simplicity to Grafana dashboard creation and to give users easy way how they can create dashboard
templates filled with different configuration.

## Installation

To install:

```
sudo pip install grafana-dashboard-builder
```
or
```
sudo python setup.py install
```

## Usage

After installation you'll find `grafana-dashboard-builder` on your path. Help can be printed by `--help` command-line
option.

```
usage: grafana-dashboard-builder [-h] -p PATH [PATH ...] [--project PROJECT] [-o OUT] [-c CONFIG]
                                 [--context CONTEXT] [--plugins PLUGINS [PLUGINS ...]]
                                 [--exporter EXPORTERS [EXPORTERS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH [PATH ...], --path PATH [PATH ...]
                        List of path to YAML definition files
  --project PROJECT     (deprecated, use path) Location of the file containing
                        project definition.
  -o OUT, --out OUT     (deprecated, use config file and file exporter) Path
                        to output folder
  -c CONFIG, --config CONFIG
                        Configuration file containing fine-tuned setup of
                        builder's components.
  --context CONTEXT     YAML structure defining parameters for dashboard
                        definition. Effectively overrides any parameter
                        defined on project level.
  --plugins PLUGINS [PLUGINS ...]
                        List of external component plugins to load
  --exporter EXPORTERS [EXPORTERS ...]
                        List of dashboard exporters
```

To start you need to create project configuration that needs to be in one YAML document. And some examples with current
full capabilities can be found in [sample project](samples/project.yaml).

## Exporters

_grafana-dashboard-builder_ provides several builtin exporters that can be enabled through `--exporter` option.
Configuration for all of them is to be provided in configuration file given in `--config` option. Look at
[sample config](samples/config.yaml).

### File exporter

File exporter is used when you want to store dashboards as JSON files on your local disk.

```yaml
file:
  output_folder: /some/directory/on/my/disk
```

To use file exporter run _grafana-dashboard-builder_ with `--exporter file` option.

### Grafana Elastic Search

_grafana-dashboard-builder_ currently supports persisting dashboards to _Elastic Search_ used by _Grafana_ prior
to version 2.0

To configure _Elastic Search_ endpoint put following structure to your configuration file:

```yaml
elastic-search:
  host: https://this-is-my-domain.com
  password: my_password
  username: my_username
```

With this configuration your dashboard will be uploaded to `https://this-is-my-domain.com/es/grafana-dash/dashboard/dashboard_name`

If you do not want to store your credentials in the configuration file you can use environment variables `ES_PASSWORD`
and `ES_USERNAME`.

To use elastic search exporter run _grafana-dashboard-builder_ with `--exporter elastic-search` option.

### Grafana API

_grafana-dashboard-builder_ currently supports _Grafana_ version 2.0 API.

To configure _Grafana_ endpoint put following structure to your configuration file:

```yaml
grafana:
  host: https://this-is-my-domain.com
  password: my_password
  username: my_username
```

With this configuration your dashboard will be POSTed to `https://this-is-my-domain.com/api/dashboards/db`

If you do not want to store your credentials in the configuration file you can use environment variables
`GRAFANA_PASSWORD` and `GRAFANA_USERNAME`.

To use Grafana exporter run _grafana-dashboard-builder_ with `--exporter grafana` option.

## YAML definition format

Each component follows the same configuration format. Top level must contain 2 fields - name and component type.
Under component type is wrapped definition of the component.

```yaml
- name: some-name
  component-type:
    component-param1: param-value
    component-param2: other-value
```

Components can be defined in multiple source files that are passed through `--path` option. If a path is directory
it is recursively walked and all files are processed.

### Components

Components define basic building blocks such as rows, graphs and template queries. They can be defined in-place or be
named and reused within other components and dashboards.

Components can define parameters that can be passed from parent component to its children.

```yaml
- name: graph-name
  panels:
    - graph:
        target: target
        y_formats: [bytes, short]
        span: 4
```

```yaml
- name: row-name
  rows:
    - row:
        title: Placeholder row
        panels:
            - graph-name
            - graph:
                target: target
                y_formats: [bytes, short]
                span: 4
```

Another component is template queries that allow you to define just one query string for hierarchical variables. Each
query part that starts with $ sign will appear as one variable.

```yaml
- name: template-name
  templates:
    - query:
        query: '{metric-prefix}.$component.$application'
```

### Dashboard

Dashboard is top-level object composed of several components.

```yaml
- name: overview
  dashboard:
    title: overview dashboard
    time_options: [1h]
    refresh_intervals: [5m]
    templates:
      - template-name:
            metric-prefix: '{metric-prefix}'
    time:
      from: now-12h
      to: now
    rows:
      - row-name
```

### Project

Project is an entry point for builder and defines which dashboards will be generated and provides parameters to them.

```yaml
- name: Example project
  project:
    dashboard-prefix: MyApp
    metric-prefix: metric.prefix
    dashboards:
        - overview
```

The biggest benefit of _grafana-dashboard-builder_ is that you can generate several dashboards from one dashboard
template just by defining multiple values for a parameter that is contained in dashboard name. Following project will
generate 2 dashboards named _prefix1-dashboard_ and _prefix2-dashboard_. 

```yaml
- name: Example project
  project:
    dashboard-prefix:
      - prefix1
      - prefix2
    dashboards:
      - '{dashboard-prefix}-dashboard'
```

## External context definition

Thanks to _project_ component you can use one dashboard template and configure it with different parameters. But what
if you need to use different params based on the _Grafana_ you are uploading dashboards to. That's why you can define
configuration externally to your projects and dashboard templates.

You can reference configuration stored in YAML with `-config` option or even inline it to `--context` option. External
configuration file can look like:

```yaml
context:
  region: eu
  default-datacenter: cze
```
