# Hypnos

Données concernant les nuits passées (coucher, lever, temps de sommeil, endroit, ...).

## Env file

Set up environment variables in a dedicated file, e.g. `my-vars.env`. See `environ-sample.env` for an example.

See how to use this env file below, either for development or to run the Docker image.

## Setup and development

```
poetry install
poetry shell
FLASK_ENV=development flask --env-file my-vars.env run
```

## Docker

The docker image exposes a wsgi application through a socket. A way to easily run it locally would be to use a 
```
docker build . -t hypnos:x.y.z
docker run --env-file my-vars.env -v hypnos_data:/data -v hypnos_socket:/shared hypnos:x.y.z
```

## Flask-Migrate notes

This project uses SQLite, which has limited implementation of `ALTER TABLE` statements.
Here is a blog post from `Flask-Migrate`'s author on how to work around those limitations: https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite
