import pandas as pd

communities = ['sustainable', 'generic']
type = ['diachronic', 'diastratic']

def merge_pmw(type):
    if type == "diachronic":
        for community in communities:
            df0 = pd.read_csv(community + "_t0_keywords_frequency.csv")
            df1 = pd.read_csv(community + "_t1_keywords_frequency.csv")
            print(df0)
            print(df1)
    
            # Excluding words with occurrences < 10
            df0 = df0[df0['raw frequency'] >= 10]
            df1 = df1[df1['raw frequency'] >= 10]
    
            # Merge DataFrames on the 'word' column to get common words
            common_words_df = pd.merge(df0, df1, on='word', how='inner', suffixes=('_t0', '_t1'))
    
            # Extract columns for pmw for the common words
            result_df = common_words_df[['word', 'pmw_t0', 'pmw_t1']]
    
            # Rename columns
            result_df.columns = ['word', 't0', 't1']
    
            result_df['change'] = result_df['t1'] - result_df['t0']
    
            # Display the result DataFrame
            print(result_df)
    
            # Write the result DataFrame to a new csv file
            result_df.to_csv(output_folder+community+'_'+type'_keywords_frequency.csv', index=False)
      
    elif type == "diastratic":
        df_sustainable = pd.read_csv("sustainable_keywords_frequency.csv")
        df_generic = pd.read_csv("generic_keywords_frequency.csv")

        # Excluding words with occurrences < 10
        df_sustainable = df_sustainable[df_sustainable['raw frequency'] >= 10]
        df_generic = df_generic[df_generic['raw frequency'] >= 10]

        # Merge DataFrames on the 'word' column to get common words
        common_words_df = pd.merge(df_sustainable, df_generic, on='word', how='inner', suffixes=('_sustainable', '_generic'))

        # Extract columns for pmw for the common words
        result_df = common_words_df[['word', 'pmw_sustainable', 'pmw_generic']]

        # Rename columns
        result_df.columns = ['word', 'sustainable', 'generic']

        result_df['change'] = result_df['sustainable'] - result_df['generic']

        # Display the result DataFrame
        print(result_df)

        # Write the result DataFrame to a new csv file
        result_df.to_csv(output_folder+type'_keywords_frequency.csv', index=False)

