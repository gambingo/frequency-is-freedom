from tracemalloc import stop
import numpy as np
import pandas as pd
import streamlit as st

from numpy import random
random = random.RandomState(42)

from .text import TEXT
import src.gtfs as gtfs
from src.graphs import download_graph_from_address


################################ App Logic ################################

def write_text(section_title, header_level=3):
    # st.subheader(section_title)
    header_hashes = "#"*header_level
    st.markdown(f"{header_hashes} {section_title}")
    for paragraph in TEXT[section_title]:
        st.write(paragraph)


############################# Bus Arrival Rates #############################

@st.cache
def load_needed_tables():
    trips = gtfs.load_prepared_gtfs_table("trips")
    stop_times = gtfs.load_prepared_gtfs_table("stop_times")
    stops = gtfs.load_prepared_gtfs_table("stops")
    return trips, stop_times, stops


def how_often_does_the_bus_come(stop_times, stops):
    # st.markdown("**Bus Arrivals per Hour**")
    st.markdown("##### Bus Arrivals per Hour")
    col1, col2 = st.columns(2)
    
    # The 50 bus
    stop_id = 8920
    bus_arrivals_per_hour(stop_times, stops, stop_id, col1, "The 50 Bus")

    # The 66 bus
    stop_id = 552
    bus_arrivals_per_hour(stop_times, stops, stop_id, col2, "The 66 Bus")


def bus_arrivals_per_hour(stop_times, stops, stop_id, st_col, ttl):
    chart_df = bus_stop_histogram(stop_times, stop_id)
    layer_spec = bus_stop_histogram_layer_spec(stops, stop_id, ttl)
    
    spec = {
        # "title":    "Chart Main Title",
        "layer":    layer_spec,
    }
    st_col.vega_lite_chart(data=chart_df, spec=spec, use_container_width=True)


def bus_stop_histogram_layer_spec(stops, stop_id, ttl):
    stop_desc = stops[stops["stop_id"] == stop_id]["stop_desc"].iloc[0]
    stop_name = stop_desc.split(",")[0].strip()
    direction = stop_desc.split(",")[1].strip()

    histogram_spec = {
        "mark": "bar",
        "title": [ttl, f"{direction} from {stop_name}"],
        "encoding": {
            "x": {
                "field": "Hour of Arrival", 
                "type": "ordinal",
                "axis": {"labelAngle": 0},
            },
            "y": {
                "field": "Buses Per Hour",
                "type": "quantitative",
                "title": "No. Buses per Hour",
            },
        }
    }
    rule_spec = {
        "mark": "rule",
        "encoding": {
            "y": {
                "field": "Buses Per Hour",
                "aggregate":    "mean",
                },
            "size": {"value": 2},
        }
    }
    layer_spec = [histogram_spec, rule_spec]
    return layer_spec


def bus_stop_histogram(stop_times, stop_id):
    # Chart Data
    chart_df = stop_times[stop_times["stop_id"] == stop_id]
    chart_df = chart_df["hour_of_arrival"].value_counts().sort_index()
    chart_df = pd.DataFrame(chart_df).reset_index()
    chart_df.rename(columns={
        "index": "Hour of Arrival",
        "hour_of_arrival": "Buses Per Hour"},
        inplace=True)
    return chart_df


######################## Wait Time Simulation ########################

def generate_bus_and_people_times(bus_frequency, num_days=7, people_per_day=1000):
    """
    Originally, I generated bus times by sampling from a poisson distribution 
    and adding those wait times up consecutively to get the bus arrival times. 
    This produced bus times that averaged to the right frequency, but the 
    average wait times for people came to half the bus frequency. I was 
    perplexed, and still don't quite understand why, but plenty of research has 
    confirmed that the probabalistically correct wait times should equal the 
    bus arrival rate, and that sampling bus arrival times randomly from a 
    uniform distribution gets the same distribution as sampling from a poisson 
    distribution.
    """
    time_length = num_days * 24 * 60 #one week
    num_buses = time_length // bus_frequency
    num_people = people_per_day * num_days

    # It was not what I first expected
    bus_times = num_buses * bus_frequency * random.random(num_buses)
    people_times = bus_times.max() * random.random(num_people)
    bus_times = np.sort(bus_times)
    people_times = np.sort(people_times)
    return bus_times, people_times


def plot_simulated_arrival_times(bus_arrivals, people_arrivals):
    # Let's zoom in to two hours, between
    ten_am = 60 * 10
    one_pm = 60 * 12
    bus_arrivals = bus_arrivals[(bus_arrivals > ten_am) & (bus_arrivals < one_pm)]
    people_arrivals = people_arrivals[(people_arrivals > ten_am) & (people_arrivals < one_pm)]

    format_timestamp = lambda mins: f"5 Sep 2022 {int(mins//60)}:{int(mins%60)}:00"
    times = []
    category = []
    for time in bus_arrivals:
        times.append(format_timestamp(time))
        category.append("Bus Arrival")

    for time in people_arrivals:
        times.append(format_timestamp(time))
        category.append("People Arrivals")
    
    df = pd.DataFrame()
    df["Arrivals"] = times
    df["Category"] = category

    histogram_spec = {
        "mark": "bar",
        "transform": [{"filter": "datum.Category == 'People Arrivals'"}],
        "format": {
            "parse": {"Arrivals": "utc:'%d %b %Y %H:%M:%S'"}
            },
        "encoding": {
            "x": {
                "timeUnit": {
                    "unit": "hoursminutes",
                    "step": 2,
                },
                "field":    "Arrivals", 
                "title": "Time",
                "axis": {"tickCount": 10},
            },
            "y": {
                "aggregate": "count",
                "title": ["No. People Arriving", "at the Bus Stop"],
                "axis": {"tickMinStep": 1},
            },
            "color": {
                "field": "Category", 
                "type": "nominal", 
                "scale": {"range": ["#31333f", "#1f77b4"]},
            },
        }
    }
    rule_spec = {
        "mark": "rule",
        "transform": [{"filter": "datum.Category == 'Bus Arrival'"}],
        "encoding": {
            "x": {
                "timeUnit": "hoursminutes",
                "field": "Arrivals", 
            },
            "size": {"value": 2},
            "color": {
                "field": "Category", 
                "type": "nominal", 
                "scale": {"range": ["#31333f", "#1f77b4"]},
            },
        }
    }
    spec = {
        "title": "Two Hours of Simulated People Waiting for a Simulated Bus",
        "height": 200,
        "layer": [histogram_spec, rule_spec]
    }
    st.vega_lite_chart(data=df, spec=spec, use_container_width=True)


def bus_time_metrics(bus_times, people_times):
    avg_btwn_time = np.mean(np.diff(bus_times))
    avg_wait_time = average_wait_time(bus_times, people_times)

    col1, col2 = st.columns(2)
    col1.metric("Average Time Between Buses", f"{round(avg_btwn_time, 1)} min")
    col2.metric("Avg. Passenger Wait", f"{round(avg_wait_time, 1)} min")


def average_wait_time(bus_times, people_times):
    ii = np.searchsorted(bus_times, people_times, side="right")
    wait_times = bus_times[ii] - people_times
    return wait_times.mean()


############################### Map Building ###############################

def address_input():
    address = st.text_input("Address", 
        key="address", 
        value="626 W Jackson Blvd, Chicago, IL 60661")
    street_address = address.split(",")[0]
    st.session_state["street_address"] = street_address


def download_walking_graph(address):
    """
    TKTK
    """
    initial_radius = 2.75 #miles
    graph, lat_lng = download_graph_from_address(address, initial_radius)
    return graph, lat_lng


def isochrone_download_button():
    with open("plots/isochrone.png", "rb") as image_file:
        st.download_button("Download Map", 
            data=image_file,
            file_name=f"{st.session_state['street_address']}.png",
            mime="image/png")