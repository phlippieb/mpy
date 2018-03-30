#! /bin/bash
#
# Postgres client:
sudo apt-get update
sudo apt-get install -y postgresql-client
#
# Postgres proxy:
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances="psodroc-db-2"=tcp:5432 &
#
# Conda:
wget -c http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh  -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda install numpy scipy numba pytest matplotlib pytest psycopg2
#
# The project:
git clone https://github.com/phlippieb/mpy.git

