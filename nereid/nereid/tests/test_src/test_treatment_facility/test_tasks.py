import pytest

from nereid.src.treatment_facility.tasks import initialize_treatment_facilities


@pytest.mark.parametrize(
    "ctxt_key, has_met_data",
    [("default", True), ("default_api_no_tf_joins_valid", False)],
)
def test_construct_nodes_from_treatment_facility_request(
    contexts, valid_treatment_facilities, ctxt_key, has_met_data
):

    context = contexts[ctxt_key]
    tmnt_facilities = {"treatment_facilities": valid_treatment_facilities}
    treatment_facilities = initialize_treatment_facilities(
        tmnt_facilities, context=context
    )

    tmnt_lst = treatment_facilities["treatment_facilities"]

    assert len(tmnt_lst) == len(valid_treatment_facilities)

    for n in tmnt_lst:
        if has_met_data:
            assert n.get("rain_gauge") is not None
        else:
            assert n.get("rain_gauge") is None


@pytest.mark.parametrize(
    "ctxt_key, has_met_data",
    [("default", True), ("default_api_no_tf_joins_valid", False)],
)
@pytest.mark.parametrize(
    "model,checkfor",
    [
        ("PermPoolFacility", "retention_volume_cuft"),
        ("RetAndTmntFacility", "retention_volume_cuft"),
        ("BioInfFacility", "retention_volume_cuft"),
        ("FlowAndRetFacility", "retention_volume_cuft"),
        ("RetentionFacility", "retention_volume_cuft"),
        ("TmntFacility", "treatment_volume_cuft"),
        ("CisternFacility", "design_storm_depth_inches"),  # TODO
        ("DryWellFacility", "retention_volume_cuft"),
        ("LowFlowFacility", "design_storm_depth_inches"),  # TODO
        ("FlowFacility", "design_storm_depth_inches"),  # TODO
        ("NTFacility", "design_storm_depth_inches"),
    ],
)
def test_construct_nodes_from_treatment_facility_request_checkval(
    contexts, valid_treatment_facility_dicts, ctxt_key, has_met_data, model, checkfor
):

    context = contexts[ctxt_key]
    tmnt_facilities = {"treatment_facilities": [valid_treatment_facility_dicts[model]]}

    treatment_facilities = initialize_treatment_facilities(
        tmnt_facilities, context=context
    )
    tmnt_lst = treatment_facilities["treatment_facilities"][0]

    check_val = tmnt_lst.get(checkfor)
    assert isinstance(check_val, float)
    assert tmnt_lst.get("errors") is None

    if has_met_data:
        assert tmnt_lst.get("rain_gauge") is not None
    else:
        assert tmnt_lst.get("rain_gauge") is None
