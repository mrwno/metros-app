# metros-app

Data are available on https://zenodo.org/records/1186215

School project in python / postgreSQL
Before Starting add your database informations in mapmetros.py
Our database is the number 61.

To lauch the application you have to type :
- `python3 mapmetros.py`

Request using Hop 3 might be a little bit long, you can see on the terminal the advancement in the terminal.

In case Request doesn't work, follow instruction below.
In the metros-app directory execute those command line :

- `python3 myparseCSV_bus.py >> bus_data.sql`
- `python3 myparseCSV_subway.py >> subway_data.sql`
- `python3 myparseCSV_tram.py >> tram_data.sql`
- `python3 myparseCSV_rail.py >> rail_data.sql`
- `python3 myparseCSV_walk.py >> walk_data.sql`
- `python3 myparseCSV_combined.py >> combined_data.sql`
- `python3 myparseCSV_paristo.py >> paristo_data.sql`
- `python3 myparseCSV_nodes.py >> nodes_data.sql`

Then connect to our database by typing :
- `psql -h postgre -U l3info_61`

If necessary you can delete every table by using :
- `drop table bus, nodes, tram, rail, subway, paris_to, historique, walk, combined;`

Then you have to recreate table by using :
- `\i database_schema.sql`

Then you add data on those table by using :
- `\i bus_data.sql`
- `\i subway_data.sql`
- `\i tram_data.sql`
- `\i rail_data.sql`
- `\i walk_data.sql`
- `\i combined_data.sql`
- `\i paristo_data.sql`
- `\i nodes_data.sql`

now you can retry the first step





