import pytest
import match_energy
import numpy as np
import pandas as pd
import warnings

@pytest.fixture(scope='session') 
def load_files():
    data_path = "data/"
    Marvel_filename = "MARVEL_out_tag_nosym_test" 
    ExoMol_filename = "C2H2_states_cut_sort_tag_nosym_test"

    Marvel_data = pd.read_csv(data_path + Marvel_filename, delim_whitespace=True, header=None, index_col=15, nrows=500)
    ExMol_data = pd.read_csv(data_path + ExoMol_filename, delim_whitespace=True, header=None, index_col=20, nrows=2000)
    yield Marvel_data, ExMol_data 
    return


def test_match_single_energy(load_files):
    Marvel_energy_col = 12
    ExMol_energy_col = 1
    
    Marvel_data, ExMol_data = load_files
    Marvel_row = Marvel_data.iloc[100]
    tag = Marvel_row.name
    energy = Marvel_row[Marvel_energy_col]
    partial_ExMol = match_energy.match_single_energy(tag, energy, ExMol_energy_col, ExMol_data)

    assert(partial_ExMol.name == tag)
    assert(np.abs(partial_ExMol[1] -energy)/energy < 0.01)
    return

def test_combine_rows(load_files):
    Marvel_data, ExMol_data = load_files
    Marvel_tag_col = 15
    Marvel_energy_col = 12
    ExMol_energy_col = 1

    
    Marvel_row = Marvel_data.iloc[187]
    tag = Marvel_row.name
    energy = Marvel_row[Marvel_energy_col]
    partial_comb = match_energy.combine_rows(Marvel_row, ExMol_data, Marvel_energy_col, ExMol_energy_col)

    assert(partial_comb.name == tag)
    assert(np.abs(partial_comb.iloc[Marvel_tag_col + ExMol_energy_col] -energy)/energy < 0.01)
    return

def test_make_new_dataframe(load_files):
    Marvel_data, ExMol_data = load_files
    Marvel_tag_col = 15
    Marvel_energy_col = 12
    ExMol_energy_col = 1
    
    out_df = Marvel_data.apply(lambda x : match_energy.combine_rows(x, ExMol_data, Marvel_energy_col, ExMol_energy_col), axis=1 )

    conditions = np.abs(out_df.iloc[:,Marvel_energy_col] - out_df.iloc[:,Marvel_tag_col+ExMol_energy_col]) / (out_df.iloc[:,Marvel_energy_col] + 1e-12) < 0.01
    assert(conditions.eq(True).all())
    return

def test_not_match():
    data_path = "data/"
    Marvel_filename = "MARVEL_out_tag_nosym_test" 
    ExoMol_filename = "C2H2_states_cut_sort_tag_nosym_test"

    Marvel_data = pd.read_csv(data_path + Marvel_filename, delim_whitespace=True, header=None, index_col=15, nrows=10)
    ExMol_data = pd.read_csv(data_path + ExoMol_filename, delim_whitespace=True, header=None, index_col=20, nrows=2)

    Marvel_tag_col = 15
    Marvel_energy_col = 12
    ExMol_energy_col = 1
    
    Marvel_row = Marvel_data.iloc[5]
    tag = Marvel_row.name
    energy = Marvel_row[Marvel_energy_col]
    partial_comb = match_energy.combine_rows(Marvel_row, ExMol_data, Marvel_energy_col, ExMol_energy_col)

    assert(partial_comb.name == tag)
    #check if warning raised
    with pytest.warns(UserWarning, match=r"Warning no match for tag = .*"):
        warnings.warn("my warning", UserWarning)
    return
