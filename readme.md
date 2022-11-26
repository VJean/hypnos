# Hypnos

Données concernant les nuits passées (coucher, lever, temps de sommeil, endroit, ...).

## Flask-Migrate notes

This project uses SQLite, which has limited implementation of `ALTER TABLE` statements.
Here is a blog post from `Flask-Migrate`'s author on how to work around those limitations: https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite