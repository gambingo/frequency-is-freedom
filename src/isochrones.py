from collections import defaultdict

import osmnx as ox
import networkx as nx


import src.graphs as graphs
import src.gtfs as gtfs
from src.utils import timer_func


class WalkingIsochrone:
    def __init__(self, citywide_graph=None):
        self.citywide_graph = citywide_graph
        
        # TODO: calculate this by finding the center of the provided graph
        self.starting_lat_long = None


    def download_citywide_graph(self, address):
        network_type = "all"
        graph = ox.graph_from_place(address,
            network_type=network_type,
            retain_all=False,
            truncate_by_edge=True,
            simplify=True)

        graph = graphs.add_walking_times_to_graph(graph)
        self.citywide_graph = graph


    def make_isochrone(self, starting_lat_lon, trip_times=None, filepath=None, 
                       bgcolor="#262730"):
        """A Walking Only Isochrone"""
        if trip_times is None:
            trip_times = [15, 30, 45, 60]

        # Set a color scheme
        num_colors = len(trip_times)
        iso_colors = ox.plot.get_colors(num_colors,
            cmap='plasma', 
            start=0, 
            return_hex=True)

        # Node closest to starting address
        starting_node = graphs.get_nearest_node(
            self.citywide_graph, 
            starting_lat_lon)

        # Make subgraphs and color each by trip time
        node_colors = {}
        edge_colors = {}
        trip_times = sorted(trip_times, reverse=True)
        furthest_walking_graph = None
        for trip_time, color in zip(trip_times, iso_colors):
            subgraph = self.make_subgraph(starting_node, trip_time)
            for node in subgraph.nodes():
                node_colors[node] = color
            for edge in subgraph.edges():
                edge_colors[edge] = color
            if furthest_walking_graph is None:
                furthest_walking_graph = subgraph

            # Since we go in reverse, we can reduce the city graph each time
            self.citywide_graph = subgraph

        # Plot Colors
        # graph = self.citywide_graph
        graph = furthest_walking_graph
        nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
        ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]

        # Node Size
        ns = [0 for _ in graph.nodes()]

        # Plot
        if filepath is None:
            filepath = "plots/user_isochrone.png"

        fig, ax = ox.plot_graph(graph, 
            node_color=nc, edge_color=ec, node_size=ns,
            node_alpha=0.8, node_zorder=2, bgcolor=bgcolor, edge_linewidth=0.2,
            show=False, save=True, filepath=filepath, dpi=300)
        

    def make_subgraph(self, starting_node, trip_time):
        subgraph = nx.ego_graph(
            self.citywide_graph, 
            starting_node, 
            radius=trip_time, 
            distance='travel_time')
        return subgraph



class TransitIsochrone:
    def __init__ (self, app_data_directory, city):
        """
        TKTK
        """
        self.app_data_directory = app_data_directory
        self.city = city
        self.load_data_files()


    def load_data_files(self):
        # TODO: make this selfsufficient
        self.citywide_graph = graphs.load_citywide_graph(self.city)
        nx.set_edge_attributes(self.citywide_graph, True, "display")
        filepath = self.app_data_directory / "transit_graph.pkl"
        self.transit_graph = nx.read_gpickle(filepath)


    def set_graph_weights(self, freq_multiplier, reset_city_graph=False):
        """
        The transit graph weights are the total travel times from each stop, 
        which is the sum of the time spent waiting for the bus and the time 
        spent riding the bus. We set it here so we can adjust the weights based
        on the adjusted frequency of service.
        """
        if reset_city_graph:
            self.load_data_files()
        
        for orig, dest, edge_data in self.transit_graph.edges(data=True):
            travel_time = edge_data["wait_time"]/freq_multiplier
            travel_time += edge_data["transit_travel_time"]
            self.citywide_graph.add_edge(orig, dest, travel_time=travel_time, display=False)


    def make_isochrone(self, starting_lat_lon, 
                       trip_times=None, freq_multipliers=None, 
                       filepath=None, cmap="plasma", color=None, bgcolor="#262730",
                       use_city_bounds=False, bbox=None, ax=None,
                       color_start=0, color_stop=1):
        """A Walking and Transit Isochrone!!"""
        if trip_times is None:
            trip_times = [15, 30, 45, 60]

        if freq_multipliers is None:
            freq_multipliers = [1.0]
            
        reset_city_graph = len(freq_multipliers) > 1

        trip_times = sorted(trip_times, reverse=True)
        freq_multipliers = sorted(freq_multipliers, reverse=True)
        edge_colors = {}

        # Make isochrones
        isochrones = defaultdict(dict)
        for trip_time in trip_times:
            for freq in freq_multipliers:
                graph = self.transit_isochrone(starting_lat_lon, trip_time, 
                                               freq_multiplier=freq,
                                               reset_city_graph=reset_city_graph)
                isochrones[trip_time][freq] = graph

        # Assign Edge Colors
        if len(trip_times) == 1 and len(freq_multipliers) == 1:
            graph = isochrones[max(trip_times)][max(freq_multipliers)]
            edge_colors = self.assign_edge_colors(graph, edge_colors, color)
            ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]

        else:
            if len(freq_multipliers) == 1:
                # Color Subgraphs by Trip Time
                freq = freq_multipliers[0]

                # Set a color scheme
                num_colors = len(trip_times)
                iso_colors = ox.plot.get_colors(num_colors,
                    cmap=cmap, 
                    # start=0,
                    return_hex=True)

                for trip_time, iso_clr in zip(trip_times, iso_colors):
                    subgraph = isochrones[trip_time][freq]
                    edge_colors = self.assign_edge_colors(subgraph, edge_colors, iso_clr)

            elif len(trip_times) == 1:
                # Color Subgraph by Frequency
                trip_time = trip_times[0]

                # Set a color scheme
                num_colors = len(freq_multipliers)
                iso_colors = ox.plot.get_colors(num_colors,
                    cmap=cmap,
                    # start=max(freq_multipliers),
                    # start=0, 
                    # stop=max(freq_multipliers),
                    start=color_start,
                    stop=color_stop,
                    return_hex=True)

                for freq, iso_clr in zip(freq_multipliers, iso_colors):
                    subgraph = isochrones[trip_time][freq]
                    edge_colors = self.assign_edge_colors(subgraph, edge_colors, iso_clr)

            graph = isochrones[max(trip_times)][max(freq_multipliers)]
            ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]
        
        # Plot
        if filepath is None:
            filepath = "plots/user_transit_isochrone.png"

        if use_city_bounds:
            # north = max([node[1]["y"] for node in self.citywide_graph.nodes(data=True)]) 
            # south = min([node[1]["y"] for node in self.citywide_graph.nodes(data=True)]) 
            # east = max([node[1]["x"] for node in self.citywide_graph.nodes(data=True)]) 
            # west = min([node[1]["x"] for node in self.citywide_graph.nodes(data=True)]) 
            # bbox = (north, south, east, west)
            bbox = self.get_bbox_from_graph(self.citywide_graph)

        nc = [0 for _ in graph.nodes()]
        ns = [0 for _ in graph.nodes()]

        # bgcolor = "k"
        # bgcolor = "#262730"

        if ax is None:
            _, ax = ox.plot_graph(graph, 
                node_color=nc, edge_color=ec, node_size=ns,
                node_alpha=0.8, node_zorder=2, bgcolor=bgcolor, edge_linewidth=0.2,
                show=False, save=True, filepath=filepath, dpi=300, bbox=bbox)
            bbox = self.get_bbox_from_plot(ax)
        else:
            city = ox.geocode_to_gdf('Chicago, Illinois')
            x,y = city["geometry"].iloc[0].exterior.xy
            ax.plot(x,y, color=color, linewidth=0.5)

            fig, ax = ox.plot_graph(graph, ax=ax,
                node_color=nc, edge_color=ec, node_size=ns,
                node_alpha=0.8, node_zorder=2, bgcolor=bgcolor, edge_linewidth=0.2,
                show=False, save=False, filepath=filepath, dpi=300, bbox=bbox)

            ax.set_facecolor(bgcolor)
            ax.set_axis_on() 
        
        return bbox


    def assign_edge_colors(self, subgraph, edge_colors, color):
        # print(f"Subgraph has {len(subgraph.nodes)} nodes and {len(subgraph.edges)} edges.")
        for edge_data in subgraph.edges(data=True):
            edge = (edge_data[0], edge_data[1])
            if edge_data[2]["display"]:
                edge_colors[edge] = color
            else:
                edge_colors[edge] = "none"
        return edge_colors


    # @timer_func
    def transit_isochrone(self, lat_lon, trip_time, freq_multiplier=1.0, reset_city_graph=False):
        """
        Generate one isochrone for a single set of start parameters
        """
        print(f"Tracing a transit isochrone for a {trip_time} minute trip at {freq_multiplier} times arrival rates.")
        starting_node = self.get_nearest_node(lat_lon)
        self.set_graph_weights(freq_multiplier, reset_city_graph)
        subgraph = nx.ego_graph(self.citywide_graph, starting_node, 
            radius=trip_time, 
            distance='travel_time')
        subgraph.remove_edges_from([edge for edge in self.transit_graph.edges])
        return subgraph


    def get_bbox_from_graph(self, graph):
        north = max([node[1]["y"] for node in graph.nodes(data=True)]) 
        south = min([node[1]["y"] for node in graph.nodes(data=True)]) 
        east = max([node[1]["x"] for node in graph.nodes(data=True)]) 
        west = min([node[1]["x"] for node in graph.nodes(data=True)]) 
        bbox = (north, south, east, west)
        return bbox


    def get_bbox_from_plot(self, ax):
        ylim, xlim = ax.get_ylim(), ax.get_xlim()
        north, south = ylim[1], ylim[0]
        east, west = xlim[1], xlim[0]
        bbox = (north, south, east, west)
        return bbox
    

        # self.missing_stops = []
        # self.start_positions = {starting_node: trip_time}
        # Trace the Graph
        # self.isochrone = None
        # self.walking_subgraph(starting_node, trip_time, self.isochrone)
        # return self.isochrone


    # def walking_subgraph(self, starting_node, trip_time, isochrone):
    #     """
    #     Generates a subgraph of everywere you can walk from either `starting_node`
    #     or `lat_lon` within the `trip_time`.

    #     Returns the subgraph, and a list of all transit stops with the subgraph
    #     and how much trip time is left after walking to them.
    #     """
    #     # Subgraph from this location
    #     subgraph = nx.ego_graph(self.citywide_graph, starting_node, 
    #         radius=trip_time, 
    #         distance='travel_time')

    #     if isochrone is None:
    #         self.isochrone = subgraph
    #     else:
    #         self.isochrone = nx.compose(self.isochrone, subgraph)
    #     # self.subgraphs.append(subgraph)

    #     # Reachable Transit Stops
    #     # TODO: Is there an networkx function to do this more quickly?
    #     reachable_nodes = [node for node in self.transit_graph.nodes if node in subgraph.nodes and node != starting_node]

    #     # Time Left
    #     # TODO: Again, probably a faster way.
    #     time_left = [trip_time-self.walking_time_to_stop(subgraph, starting_node, dest_node) for dest_node in reachable_nodes]

    #     # New Locations and Time Left
    #     ## this returns a nested list of dictionaries
    #     new_start_nodes_and_travel_times = [self.new_start_parameters(node, travel_time) for node, travel_time in zip(reachable_nodes, time_left)]

    #     # Prioritize


    #     # Keep going and going and going
    #     for transit_stop in new_start_nodes_and_travel_times:
    #         for starting_node, trip_time in transit_stop.items():
    #             if not self.previously_visited_this_stop(starting_node, trip_time):
    #                 self.walking_subgraph(starting_node, trip_time, self.isochrone)


    # def new_start_parameters(self, origin_node, time_left):
    #     # Where you can get and how long it will take
    #     nodes_and_times = nx.single_source_dijkstra(self.transit_graph, origin_node, 
    #         cutoff=time_left)[0]

    #     # Subtract travel time from time left
    #     nodes_and_times = {node:time_left-travel_time for node, travel_time in nodes_and_times.items() if node != origin_node}
    #     return nodes_and_times


    # def prioritize_start_locations(self, nodes_and_times):
    #     new_start_locations = []
    #     for origin_node_dict in nodes_and_times:
    #         for dest_node, time_left in origin_node_dict.items():
    #             if dest_node not in self.isochrone.nodes:
    #                 # This 
    

    # def previously_visited_this_stop(self, graph_node, trip_time):
    #     """
    #     To prevent us from riding the bus back and forth
    #     """
    #     if graph_node not in self.start_positions:
    #         self.start_positions[graph_node] = trip_time
    #         # print(f"New Transit Stop:\t\t{graph_node}\t{trip_time}")
    #         return False

    #     else:
    #         if trip_time > self.start_positions[graph_node]:
    #             self.start_positions[graph_node] = trip_time
    #             # print(f"Transit Stop with more time:\t{graph_node}\t{trip_time}")
    #             return False
        
    #     return True


    def get_nearest_node(self, location, graph=None, trip_times=None):
        """
        Used to find the center node of the graph. If there is no one closest node, 
        osmnx returns a list. Here we simply take the first node from that list. 
        All the nodes will be right on top of each other and there's no point for 
        our purposes in distinguishing between them.
        ---
        Reminder: Longitude is along the X axis. Latitude is along the Y axis. When 
        we speak we tend to say "lat long", implying latitude comes first. But 
        since latitude goes north/south and longidtude goes east/west, in an X-Y 
        coordinate system, longitude comes first. 
        """
        if graph is None:
            graph = self.citywide_graph

        lat = location[0]
        lng = location[1]
        nearest_node = ox.distance.nearest_nodes(graph, lng, lat)
    
        if not isinstance(nearest_node, int):
            nearest_node = nearest_node[0]

        return nearest_node


    def walking_time_to_stop(self, graph, origin_node, dest_node):
        path = ox.distance.shortest_path(graph, origin_node, dest_node, weight="travel_time")
        walking_time = nx.function.path_weight(graph, path, weight="travel_time")
        return walking_time
