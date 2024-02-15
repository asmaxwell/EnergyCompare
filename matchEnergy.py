"""
Created by Andy S Maxwell 14/02/2024
Script to find matching energy from different line lists
"""

import pandas as pd

def match_single_energy(tag :str, energy : float, energy_col : int, match_data : pd.DataFrame) -> pd.DataFrame:
    if tag in match_data.index:
        partial_data_temp = match_data.loc[tag,:]
        print(partial_data_temp)
        partial_data = partial_data_temp.reset_index(drop=True)
        nearest_index = partial_data.loc[:,energy_col].sub(energy).abs().idxmin()
        return partial_data.loc[nearest_index,:]
    else:
        return None
def combine_rows(Marvel_row, match_data : pd.DataFrame) -> pd.DataFrame:
    tag = Marvel_row.name
    energy = Marvel_row[12]
    return match_single_energy(tag, energy, 1, match_data)#pd.concat([Marvel_row, match_single_energy(tag, energy, 1, match_data)], axis="columns")


def main() -> None:
    data_path = "data/"
    Marvel_filename = "MARVEL_out_tag_nosym" 
    ExoMol_filename = "C2H2_states_cut_sort_tag_nosym"

    Marvel_data = pd.read_csv(data_path + Marvel_filename, delim_whitespace=True, header=None, index_col=15, nrows=1000)
    ExMol_data = pd.read_csv(data_path + ExoMol_filename, delim_whitespace=True, header=None, index_col=20, nrows=20000)

    ##test -- match_single_energy
    Marvel_row = Marvel_data.iloc[100]
    tag = Marvel_row.name
    print(tag)
    energy = Marvel_row[12]
    print(f"Marvel energy: {energy}")
    #print(ExMol_data.iloc[100])
    partial_ExMol = combine_rows(Marvel_row, ExMol_data) #match_single_energy(tag, energy, 1, ExMol_data)
    print(partial_ExMol)
    print(f"ExMol energy: {partial_ExMol[1]}")


    ### Make lambda function to apply to each row of 


    # for row in Marvel_data.iterrows():
    #     print(row.index)
    #     ExoMol_data.loc[row.index,:]

    # print(Marvel_data)


    return

#When script is run from the command line it runs this part
if __name__ == "__main__":
    main()


    


