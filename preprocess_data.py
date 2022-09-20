import matplotlib.pyplot as plt

import src.graphs as graphs
from src.isochrones import WalkingIsochrone, TransitIsochrone, timer_func
from src.filepaths import DATA_DIR


def walking_isochrone_from_my_apartment():
    print("Generating the Walking Isochrone")
    my_address = "906 N Winchester Ave, Chicago, IL 60622"
    # Please send me something nice for Christmas

    # TODO: Just take as subgraph of the chicago graph
    graph, starting_lat_lon = graphs.download_graph_from_address(my_address)

    walking_isochrone = WalkingIsochrone()
    walking_isochrone.citywide_graph = graph
    filepath = "plots/walking_isochrone_from_my_apartment.png"
    _ = walking_isochrone.make_isochrone(starting_lat_lon, filepath=filepath)


@timer_func
def transit_isochrone_from_my_apartment():
    # my_address = "906 N Winchester Ave, Chicago, IL 60622"
    # my_lat_lon = ox.geocoder.geocode(my_address)
    my_lat_lon = (41.898010150000005, -87.67613740698785)
    transit_isochrone = TransitIsochrone(DATA_DIR)

    trip_times = [15, 30, 45, 60]
    freq_multipliers = [1]
    filepath = "plots/transit_isochrone_from_my_apartment.png"
    transit_isochrone.make_isochrone(my_lat_lon, trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        cmap="plasma")


def frequency_isochrones_from_my_apartment(trip_time=30):
    my_lat_lon = (41.898010150000005, -87.67613740698785)
    transit_isochrone = TransitIsochrone(DATA_DIR)

    freq_multipliers = [0.5, 1, 2, 3]
    bgcolor="#262730"
    fig, ax = plt.subplots(nrows=1, ncols=len(freq_multipliers), 
        figsize=(3*len(freq_multipliers), 4))

    for ii, freq in enumerate(freq_multipliers):
        filepath = f"plots/frequency_isochrone_{trip_time}_min_trips.png"
        transit_isochrone.make_isochrone(my_lat_lon, 
            trip_times=[trip_time], 
            freq_multipliers=[freq],
            filepath=filepath,
            color="#B3DDF2",
            bgcolor=bgcolor,
            use_city_bounds=True,
            ax=ax[ii])
        plt.savefig(filepath, dpi=300, facecolor=bgcolor)


def frequency_grip_plot():
    """TKTKT"""
    my_lat_lon = (41.898010150000005, -87.67613740698785)
    transit_isochrone = TransitIsochrone(DATA_DIR)

    freq_multipliers = [0.5, 1, 2, 3]
    # trip_times = [30, 45, 60]
    # trip_times = [5, 10, 15]
    trip_times = [5, 10]

    bgcolor="#262730"
    fig, ax = plt.subplots(
        nrows=len(trip_times), 
        ncols=len(freq_multipliers), 
        figsize=(3*len(freq_multipliers),4*len(trip_times)))

    for ii, trip_time in enumerate(trip_times):
        for jj, freq in enumerate(freq_multipliers):
            # filepath = f"plots/frequency_isochrone_{trip_time}_min_trips.png"
            filepath = "plots/frequency_grid_plot.png"
            transit_isochrone.make_isochrone(my_lat_lon, 
                trip_times=[trip_time], 
                freq_multipliers=[freq],
                filepath=filepath,
                color="#B3DDF2",
                bgcolor=bgcolor,
                use_city_bounds=True,
                ax=ax[ii, jj])
            if jj == 0:
                ax[ii, jj].set_ylabel(f"{trip_time} min trip")
            if ii == len(trip_times)-1:
                ax[ii, jj].set_xlabel(f"{freq} time scheduled service")
            axis_formatting(ax[ii, jj], "white")
            plt.savefig(filepath, dpi=300, facecolor=bgcolor)


def axis_formatting(ax, color):
    # ax.axis("on")
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color(color) 
    ax.spines['right'].set_color(color)
    ax.spines['left'].set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)


if __name__ == "__main__":
    # Data
    # gtfs.load_clean_and_save_tables()
    # graphs.download_citywide_graph()

    # routes = gtfs.load_prepared_gtfs_table("routes")
    # trips = gtfs.load_prepared_gtfs_table("trips")
    # stop_times = gtfs.load_prepared_gtfs_table("stop_times")  
    # stops = gtfs.load_prepared_gtfs_table("stops") 

    # # # Bus Frequency
    # gtfs.average_arrival_rates_per_stop(stop_times)

    # # Match Bus Stops to OSMNX graph
    # chicago = graphs.load_chicago_graph()
    # gtfs.find_graph_node_IDs_for_transit_stop(stops, chicago)

    # Travel Time Between Transit Stops (this takes some time)
    # gtfs.average_travel_times_per_route(routes, trips, stop_times)

    # Transit Graph
    # graph = gtfs.build_transit_graph()

    # Isochrone Images
    # walking_isochrone_from_my_apartment()
    # transit_isochrone_from_my_apartment()
    frequency_isochrones_from_my_apartment()
    # frequency_maps()



