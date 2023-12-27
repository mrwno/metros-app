create table subway(
    
from_stop_I numeric, 
to_stop_I numeric,
d numeric,
duration_avg numeric,
n_vehicles numeric,
route_I_counts text,
bus_id numeric[],
route_id numeric[]
);

create table bus(
    
from_stop_I numeric, 
to_stop_I numeric,
d numeric,
duration_avg numeric,
n_vehicles numeric,
route_I_counts text,
bus_id numeric[],
route_id numeric[]
);

create table rail(
    
from_stop_I numeric, 
to_stop_I numeric,
d numeric,
duration_avg numeric,
n_vehicles numeric,
route_I_counts text,
bus_id numeric[],
route_id numeric[]
);

create table tram(
    
from_stop_I numeric, 
to_stop_I numeric,
d numeric,
duration_avg numeric,
n_vehicles numeric,
route_I_counts text,
bus_id numeric[],
route_id numeric[]
);

create table walk(
    
from_stop_I numeric, 
to_stop_I numeric,
d numeric,
d_walk numeric
);

create table combined(
    
from_stop_I numeric, 
to_stop_I numeric,
d numeric,
duration_avg numeric,
n_vehicles numeric,
route_I_counts text,
bus_id numeric[],
route_id numeric[],
route_type numeric
);

create table paris_to (
    
route_I numeric(10,6),
route_name text ,
route_type numeric(10,6)

);

create table historique (
id SERIAL PRIMARY KEY,
from_station text ,
to_station text ,
nb_hop numeric ,
moyen text 
)
