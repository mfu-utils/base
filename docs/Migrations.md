# Migrations
Using SqlAlchemy + alembic

### Other docs:
* [Seeders](Seeders.md)
* [CI](CI.md)
* [Readme](../README.md)


### Create fresh database

!!! Before run commands you need will delete `db` file and all alembic migrations files.

```shell
   alembic revision --autogenerate -m 'initial' # Create new first migration file
   alembic upgrade head # Load migration into db
```

After that result `db/migrations/XXXXXXXXXXXX_initial.py`
