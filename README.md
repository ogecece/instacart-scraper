# Instacart Scraper

Simple spider and workflow system for scraping Instacart's (US) default store
for a given user.

## Table of Contents
  * [How to run](#how-to-run)
  * [How to check collected data](#how-to-check-collected-data)
  * [How to destroy the created environment](#how-to-destroy-the-created-environment)
  * [For developers](#for-developers)

## How to run

First, you have to setup your environment variables. Samples
([`.env.sample`](.env.sample) and [`.db.env.sample`](.db.env.sample)) were
provided.

Then, execute (Docker and Docker Compose are required):

```shell
$ make run
```

Done :smile:

*Note: Recaptcha solving may fail. Retries are already in place, but in rare
cases they are insufficient. In these cases, you try and run again.*

## How to check collected data

If you want to run a query in the database, execute:

```shell
$ POSTGRES_USER=<YOUR-POSTGRES-USER> QUERY=<YOUR-QUERY> make sql-query
```

However, to make things easier, a shortcut to make a `SELECT *` on all tables
is available through:

```shell
$ POSTGRES_USER=<YOUR-POSTGRES-USER> make sql-select-all
```

## How to destroy the created environment

This project uses Docker. To destroy created images, volumes, etc., execute:

```shell
$ make destroy
```

## For developers

To setup you developer environment, create a virtualenv and execute:

```shell
$ make dev-setup
```

This project uses `pre-commit` for managing code formatting and `pip-tools` to
manage dependencies.
