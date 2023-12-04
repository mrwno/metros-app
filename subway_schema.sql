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
