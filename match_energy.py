"""
Created by Andy S Maxwell 14/02/2024
Script to find matching energy from different line lists
"""

import pandas as pd
import warnings

def match_single_energy(tag :str, energy : float, energy_col : int, match_data : pd.DataFrame) -> pd.Series:
    if tag in match_data.index:
        #find matching state/ tag
        partial_data = match_data.loc[tag,:].reset_index(drop=True)    
        #if only one line matches energy level immeditately return
        if len(partial_data.shape) < 2:
            return partial_data
        
        #find nearest energy
        nearest_index = partial_data.loc[:,energy_col].sub(energy).abs().idxmin()
        return partial_data.loc[nearest_index,:].rename(tag)
    else:
        warning_message = f"Warning no match for tag = {tag}, and energy = {energy}"
        warnings.warn(UserWarning(warning_message) )
        return pd.Series( [0]*match_data.shape[1] , name=tag )
    
def combine_rows(Marvel_row : pd.Series, match_data : pd.DataFrame, Marvel_energy_col : int, ExMol_energy_col : int) -> pd.Series:
    tag = Marvel_row.name
    energy = Marvel_row[Marvel_energy_col]
    return pd.concat([Marvel_row, match_single_energy(tag, energy, ExMol_energy_col, match_data)], axis=0).rename(tag)


def main() -> None:
    data_path = "data/"
    Marvel_filename = "MARVEL_out_tag_nosym" 
    ExoMol_filename = "C2H2_states_cut_sort_tag_nosym"
    out_filename = Marvel_filename + "_" + ExoMol_filename

    Marvel_tag_col = 15
    ExMol_tag_col = 20
    Marvel_energy_col = 12
    ExMol_energy_col = 1

    print("Loading data")
    Marvel_data = pd.read_csv(data_path + Marvel_filename, delim_whitespace=True, header=None, index_col=Marvel_tag_col
                              , nrows=5000
                              )
    ExMol_data = pd.read_csv(data_path + ExoMol_filename, delim_whitespace=True, header=None, index_col=ExMol_tag_col
                             , nrows=50000
                             )

    print("Matching data")
    out_df = Marvel_data.apply(lambda x : combine_rows(x, ExMol_data, Marvel_energy_col, ExMol_energy_col), axis=1 )
    print("Example of matched energies:")
    print(out_df.iloc[:,[12,16]])
    out_df.to_csv(data_path + out_filename, sep=' ', header=False)
    

    return

#When script is run from the command line it runs this part
if __name__ == "__main__":
    main()


    


