"""
This file is designed to clean the data for preprocessing, for example:
    Drop NA Columns or empty columns
    Drop unecessary columns (Description, etc.)
"""
import numpy as np
import pandas as pd

class dataCleaner:
    
    def __init__(self,id):
        self.id = id
    
    def open_file(self):
        print("Cleaning Data For:",self.id)
        pitcher_df = pd.read_csv(f"data/unclean/{self.id}.csv")
        clean_df = pitcher_df[["pitch_type","release_speed","release_pos_x","release_pos_z","spin_dir","spin_rate_deprecated","break_angle_deprecated","break_length_deprecated","zone","stand","p_throws","type","balls","strikes","pfx_x","pfx_z","plate_x","plate_z","on_3b","on_2b","on_1b","outs_when_up","inning","vx0","vy0","vz0","ax","ay","az","sz_top","sz_bot","release_spin_rate","release_extension","release_pos_y","at_bat_number","pitch_number","pitch_name","spin_axis"]]
        
        "Everything above 10 gets shifted down by 2"
        
        #clean_df.drop(clean_df[clean_df['zone'] == 14].index,inplace=True)
        #clean_df.to_csv(f"data/clean/{self.id}.csv")
        
        # Shift the zones below 10 down by 1
        clean_df.loc[clean_df['zone'] < 10, 'zone'] = clean_df['zone'] - 1
        
        # Shift the zones above 10 down by 2
        clean_df.loc[clean_df['zone'] > 10, 'zone'] = clean_df['zone'] - 2
        
        # Save the updated clean_df
        clean_df.to_csv(f"data/clean/{self.id}.csv", index=False)
        print(f"Cleaning for file {self.id}, has been finished!")

p1 = dataCleaner(656302)
p1.open_file()