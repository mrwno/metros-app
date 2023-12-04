create table subway(
    
from_stop_I numeric(10,6), 
to_stop_I numeric(10,6),
d numeric(10,6),
duration_avg numeric(10,6),
n_vehicles numeric(10,6),
route_I_counts text,
bus_id numeric[],
route_id numeric[]
);

create table bus(
    
from_stop_I numeric(10,6), 
to_stop_I numeric(10,6),
d numeric(10,6),
duration_avg numeric(10,6),
n_vehicles numeric(10,6),
route_I_counts text,
bus_id numeric[],
route_id numeric[]
);
