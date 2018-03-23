This library uses PostgreSQL to persist results/measurements. This readme assumes MacOS.

# Installing

Install PostgreSQL using homebrew:

```
brew install postgresql
```

# Setup

This library assumes an existing database schema. Create the schema as follows.

## Create the database

Start PostgreSQL using homebrew:

```
brew services start postgresql
```

(To stop the database, run `brew services stop postgresql`).

The database should have you as a user, but if you like, you can create a new one:
```
createuser -sP <username>
```
Take note of your username.

Create the database, naming yourself the owner:

```
createdb -O <username> psodroc
```

Fire up the PostgreSQL command line tool:

```
psql -U <username> psodroc
```

Then, within the `psql` shell, create the tables needed by the library; see `create_tables.sql` in this directory for commands with schema descriptions.

Lastly, within the Python scripts, PostgreSQL is accessed using `psycopg2`. Install using anaconda:

```
conda install psycopg2
```
