import pandas as pd
import os

input_dir = "/home/p311477/Desktop/milk_project/DH_project/comments_no_noise/"
output_dir = "/home/p311477/Desktop/milk_project/DH_project/time_slots_comments/"

communities = ['sustainable', 'generic']
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

all_files =os.listdir(input_dir)
all_files.sort()

def create_corpora(input_folder, output_folder,type):
    for community in communities:
        to_merge = []
        
        for filename in all_files:          
            if community in filename:
                if type == "all":
                  # Create communities corpora
                  if any(str(year) in filename for year in years):
                      df = pd.read_csv(input_dir+filename)
                  
                      # Drop the 'id' column
                      df.drop(columns=['id'], inplace=True)
                      df = df.dropna()
                      
                      # Append the dataframe to the list
                      to_merge.append(df)
                elif type == "t0" and community == "sustainable":
                    # Create sustainable t0
                    if any(str(year) in filename for year in years[:7]):
                        df = pd.read_csv(input_dir+filename)
                    
                        # Drop the 'id' column
                        df.drop(columns=['id'], inplace=True)
                        df = df.dropna()
                        
                        # Append the dataframe to the list
                        to_merge.append(df)
                elif type == "t0" and community == "generic":
                    # Create generic t0
                    if any(str(year) in filename for year in years[:5]):
                        df = pd.read_csv(input_dir+filename)
                    
                        # Drop the 'id' column
                        df.drop(columns=['id'], inplace=True)
                        df = df.dropna()
                        
                        # Append the dataframe to the list
                        to_merge.append(df)
                elif type == "t1":
                    if any(str(year) in filename for year in years[11:]):
                        df = pd.read_csv(input_dir+filename)
                    
                        # Drop the 'id' column
                        df.drop(columns=['id'], inplace=True)
                        df = df.dropna()
                        
                        # Append the dataframe to the list
                        to_merge.append(df)
                  
        # Merge CSV files
        merged_dfs = pd.concat(to_merge,ignore_index=True)

        # Write merged CSV to a new file
        if type ==all:
            merged_dfs.to_csv(output_dir+community+'.csv', index=False)
        elif type == "t0":
            merged_dfs.to_csv(output_dir+community+'_t0.csv', index=False)
        elif type == "t1":
            merged_dfs.to_csv(output_dir+community+'_t1.csv', index=False)

input_folder =""
output_folder=""
type="" #'t0' or 't1' or 'all'

create_corpora(input_folder,output_folder,type)





