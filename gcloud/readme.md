# Setup on Google Cloud Platform

This readme contains instructions for setting up the experiments on Google Cloud Platform. The setup uses one dedicated instance for a PostgreSQL database, for storing and retrieving results, and one for the computations/simulations. Before you follow this guide, you should already have an account on GCP.

## Command line tools

1. Install the command line tools ([instructions](https://cloud.google.com/sdk/downloads)).

## Setup the database instance

1. Create an SQL instance.
    - Use PostgreSQL.
    - Note the `<db-instance-id>` as the instance id/name of this db instance.
    - Generate a password for the `postgres` user and paste it somewhere.
    - Note the `zone`.
    - Note the `<db-connection_id>`, which is different from the instance id.
2. Go to the SQL instance's details on the (web) console.
    - Go to the USERS tab and create a user named `psodroc` with password `psodroc`.
    - Go to the DATABASES tab and create a database named `psodroc`.
3. Connect.
    - From your terminal (where the command line tools are installed), run 
        ```
        gcloud sql connect <db-instance-id> --user psodroc
        ```
    where `<db-instance-id>` is the instance id you noted before. The password is `psodroc`. You should now be signed into a psql terminal client.

4. Copy SQL from [create-table.sql](https://github.com/phlippieb/mpy/blob/master/db/create_tables.sql). Paste it into the psql client.
5. Quit the psql client (`\q`).

## Setup the compute engine instance

1. Create a compute engine instance.
    - Choose the same zone used for the SQL instance.
    - Choose Ubuntu 16.04.
    - Under _Cloud API access scopes_, enable _Cloud SQL_.
    - Note the `<c-instance-id>` as the id/name of this compute engine instance.
2. Connect.
    - From the view of all compute instances, under the _connect_ column, click the dropdown next to _SSH_.
    - Select _View gcloud command_.
    - Run the command in terminal.
3. Set up the connection to the SQL instance.
    - ([Instructions](https://cloud.google.com/sql/docs/postgres/connect-compute-engine#gce-connect-proxy)).
    - Install the psql client from the package manager:
        ```
        sudo apt-get update
        sudo apt-get install postgresql-client
        ```
    - Install the Cloud SQL Proxy on the Compute Engine instance:
        ```
        wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
        chmod +x cloud_sql_proxy
        ```
    - Start the proxy. You may want to do this in a tmux session.
        ```
        ./cloud_sql_proxy -instances="<db-connection-id>"=tcp:5432
        ```
        where `<db-connection-id>` is the connection id for the db that you noted before; **note** that this is not the instance id!
    - Detach from the tmux session, or create a new window.
    - You should now be able to connect to your SQL instance via the proxy:
        ```
        psql "host=127.0.0.1 sslmode=disable dbname=psodroc user=psodroc"
        ```
        The password is `psodroc`.
4. Setup Python, Anaconda, and Mpy.
    - Verify that Python2.7 is installed with `python -V`.
    - Install miniconda:
        ```
        wget -c http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
        chmod +x Miniconda-latest-Linux-x86_64.sh
        ./Miniconda-latest-Linux-x86_64.sh
        ```
        Follow the prompts. Source the new path with `source .bashrc`.
    - Install project dependencies:
        ```
        conda install numpy scipy numba pytest matplotlib pytest psycopg2
        ```
    - Clone the project:
        ```
        git clone https://github.com/phlippieb/mpy.git
        ```
5. Run!
    - Go to the project root (`cd mpy`).
    - Choose to either `make run` (everything on one processor), or do other things, such as:
        ```
        # Make the DRoC measurements that will be used by the ranks:
        python run.py --prep
        
        # Run the 1st of 8 batches (note: zero-index):
        # python run.py --batch 0 --of 8
        ```
    
