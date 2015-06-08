# grafana-dashboard-builder

[![Build Status](https://travis-ci.org/jakubplichta/grafana-dashboard-builder.svg?branch=master)](https://travis-ci.org/jakubplichta/grafana-dashboard-builder) [![Coverage Status](https://coveralls.io/repos/jakubplichta/grafana-dashboard-builder/badge.svg?branch=master)](https://coveralls.io/r/jakubplichta/grafana-dashboard-builder?branch=master)

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

After installation you'll find `grafana_dashboard_builder.py` on your path. Help can be printed by `--help` command-line
option.

```
usage: grafana_dashboard_builder.py [-h] -p PROJECT [-o OUT]
                                    [--plugins PLUGINS [PLUGINS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Location of the file containing project definition.
  -o OUT, --out OUT     Path to output folder
  --plugins PLUGINS [PLUGINS ...]
                        List of external component plugins to load
```

To start you need to create project configuration that needs to be in one YAML document. And some examples with current
full capabilities can be found in [sample project](samples/project.yaml).

### YAML format

Each component follows the same configuration format. Top level must contain 2 fields - name and component type.
Under component type is wrapped definition of the component.

```yaml
- name: some-name
  component-type:
    component-param1: param-value
    component-param2: other-value
```

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
