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

The docker image exposes a wsgi application through http, so that a NGINX reverse-proxy is easy to plug in.
```
docker build . -t hypnos:x.y.z # add --load when using buildx
# multi-arch build: docker buildx build --platform linux/amd64,linux/arm64 --load -t hypnos:0.1.0 .
docker run --env-file my-vars.env -v hypnos_data:/data hypnos:x.y.z
```

## Flask-Migrate notes

This project uses SQLite, which has limited implementation of `ALTER TABLE` statements.
Here is a blog post from `Flask-Migrate`'s author on how to work around those limitations: https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite
