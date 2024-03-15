import pytest
import A_GIS.Code.Unit.Name.fix


def test_fix_standard_case():
    assert (
        A_GIS.Code.Unit.Name.fix(name="A_GIS.Data.Pre_Processing.Clean_Data")
        == "A_GIS.Data.PreProcessing.clean_data"
    )


def test_fix_incorrect_first_part():
    assert (
        A_GIS.Code.Unit.Name.fix(name="incorrect.Data.Pre_Processing.Clean_Data")
        == "A_GIS.Incorrect.Data.PreProcessing.clean_data"
    )


def test_fix_lowercase_function_name():
    assert (
        A_GIS.Code.Unit.Name.fix(name="a_gis.Data.Pre_Processing.clean_data")
        == "A_GIS.Data.PreProcessing.clean_data"
    )


def test_fix_no_package_names():
    assert A_GIS.Code.Unit.Name.fix(name="A_GIS.clean_data") == "A_GIS.clean_data"


def test_fix_single_part():
    # This tests a scenario where the input is just a function name without A_GIS prefix.
    # Depending on the intended behavior, this might need to insert 'A_GIS' at the beginning or not.
    # The current implementation of `A_GIS.Code.Unit.Name.fix` would add 'A_GIS', treating the input as incorrect first part.
    assert A_GIS.Code.Unit.Name.fix(name="clean_data") == "A_GIS.clean_data"


def test_fix_all_caps():
    assert (
        A_GIS.Code.Unit.Name.fix(name="A_GIS.DATA.PRE_PROCESSING.CLEAN_DATA")
        == "A_GIS.DATA.PREPROCESSING.clean_data"
    )


def test_fix_mixed_case_with_underscores():
    assert (
        A_GIS.Code.Unit.Name.fix(name="A_GIS.DaTa_Pre_Processing.Clean_DATA")
        == "A_GIS.DaTaPreProcessing.clean_data"
    )


# Optionally, you can include a test to ensure that the function correctly handles an already correct name
def test_fix_already_correct():
    assert (
        A_GIS.Code.Unit.Name.fix(name="A_GIS.Data.Preprocessing.clean_data")
        == "A_GIS.Data.Preprocessing.clean_data"
    )
