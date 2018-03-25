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

Lastly, within the Python scripts, PostgreSQL is accessed using `psycopg2`. This should be installed if you followed the readme in the project root. If not, install using anaconda:

```
conda install psycopg2
```

# Setup on Ubuntu server

## Install PostgreSQL using aptitude.

**Note**: on Ubuntu 14.04, aptitude does not provide PostgreSQL 9.5, which is the minimum required version for some of the commands used by this library's scripts. On Ubuntu 16.04, I think you should be fine.

### Installing on 16.04:

On 16.04, PostgreSQL 9.5 is available, I think. Just run:
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
(Side note, I don't know if `postgresql-contrib` is actually useful.)

### Installing on 14.04:


Ensure we're up to date:
```
sudo apt-get update -y && apt-get upgrade -y
```

Edit `/etc/apt/sources.list.d/pgdg.list`:
```
sudo vi /etc/apt/sources.list.d/pgdg.list
```
(The file was empty when I did this, but it worked fine.) Then add these two lines to the file:
```
# PostgreSQL repository
deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main
```
Save and quit.

Download the repository key:
```
wget  - https://www.postgresql.org/media/keys/ACCC4CF8.asc
```
Then add the key to aptitude:
```
sudo apt-key add ACCC4CF8.asc
```
Lastly, you can remove the key, I think.
```
rm ACCC4CF8.asc
```

Update package sources again:
```
sudo apt-get update -y
```
Then install:
```
sudo apt-get install postgresql-9.5 -y
```
And you're done! Installing should have started the service by default, but you can verify that it's up by running
```
service postgresql status
```

## Create a role 

The script assumes the role of a user named `psodroc`. Create the role for the script to use:

```
sudo -u postgres createuser -sP psodroc
```

The `createuser` binary will prompt you for a password. Enter `psodroc`.

## Create a database

The script works in a databse (also) called `psodroc`. Create the database for the script to use, with the new role as the owner:

```
sudo -u postgres createdb -O psodroc psodroc
```

## Create the tables

First, check your current directory. You should be in the `mpy` root dir.
Next, open a postgres shell for the `psodroc` database as the `psodroc` role/user:

```
psql psodroc -d psodroc
```

If you get an error like "psql: FATAL:  Peer authentication failed for user "psodroc", try signing in like this:
```
psql psodroc -h localhost -d psodroc
```

You should now see a prompt like `psodroc=>`.

Lastly, from within this shell, run the `create_tables` scripts (assuming you are in the project root directory):

```
\i db/create_tables.sql
```

You should see two `CREATE TABLE` lines confirming that the tables were created. You can check that they were by entering `\d`. Quit the shell by entering `\q`.
