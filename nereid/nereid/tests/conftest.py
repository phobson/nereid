from pathlib import Path
from itertools import product
from copy import deepcopy

import pytest

from nereid.core.utils import get_request_context
from nereid.core.io import load_json
from nereid.src.land_surface.utils import make_fake_land_surface_requests


@pytest.fixture
def subgraph_request_dict():
    graph = {
        "graph": {
            "directed": True,
            "edges": [
                {"source": "3", "target": "1"},
                {"source": "5", "target": "3"},
                {"source": "7", "target": "1"},
                {"source": "9", "target": "1"},
                {"source": "11", "target": "1"},
                {"source": "13", "target": "3"},
                {"source": "15", "target": "9"},
                {"source": "17", "target": "7"},
                {"source": "19", "target": "17"},
                {"source": "21", "target": "15"},
                {"source": "23", "target": "1"},
                {"source": "25", "target": "5"},
                {"source": "27", "target": "11"},
                {"source": "29", "target": "7"},
                {"source": "31", "target": "11"},
                {"source": "33", "target": "25"},
                {"source": "35", "target": "23"},
                {"source": "4", "target": "2"},
                {"source": "6", "target": "2"},
                {"source": "8", "target": "6"},
                {"source": "10", "target": "2"},
                {"source": "12", "target": "2"},
                {"source": "14", "target": "2"},
                {"source": "16", "target": "12"},
                {"source": "18", "target": "12"},
                {"source": "20", "target": "8"},
                {"source": "22", "target": "6"},
                {"source": "24", "target": "12"},
            ],
        },
        "nodes": [{"id": "3"}, {"id": "29"}, {"id": "18"}],
    }

    return graph


@pytest.fixture(scope="module")
def land_surface_ids():

    context = get_request_context()
    ls_data = load_json(Path(context["data_path"]) / "land_surface_data.json")["data"]
    ls_ids = [dct["surface_id"] for dct in ls_data]

    yield ls_ids


@pytest.fixture(scope="module")
def land_surface_loading_response_dicts(land_surface_ids):

    n_rows = [10, 50, 5000]
    n_nodes = [5, 50, 1000]
    responses = {}

    for nrows, nnodes in product(n_rows, n_nodes):
        ls_list = make_fake_land_surface_requests(nrows, nnodes, land_surface_ids)
        ls_request = dict(land_surfaces=ls_list)

        responses[(nrows, nnodes)] = ls_request

    yield responses


@pytest.fixture
def contexts():

    cx1 = get_request_context()

    cx2 = deepcopy(cx1)
    cx2.pop("data_path")

    cx3 = deepcopy(cx1)
    cx3["data_path"] = r"¯\_(ツ)_/¯"

    cx4 = deepcopy(cx1)
    cx4.pop("project_reference_data")

    cx5 = deepcopy(cx1)
    cx5["project_reference_data"]["land_surface_table"].pop("file")

    cx6 = deepcopy(cx1)
    cx6["project_reference_data"]["land_surface_table"]["file"] = r"¯\_(ツ)_/¯"

    cx7 = deepcopy(cx1)
    cx7["project_reference_data"]["land_surface_table"] = [r"¯\_(ツ)_/¯"]

    keys = [  # these are easier to copy into tests
        "default",
        "default_no_data_path_invalid",
        "default_dne_data_path_invalid",
        "default_no_ref_data_invalid",
        "default_no_lst_file_invalid",
        "default_lst_file_dne_invalid",
        "default_lst_not_dict_invalid",
    ]

    values = [cx1, cx2, cx3, cx4, cx5, cx6, cx7]

    return {k: v for k, v in zip(keys, values)}