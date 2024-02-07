import os
import pandas as pd

def rename_columns(df):
   columns_new_names = {
       'ATP': 'atp',
       'Location': 'location',
       'Tournament': 'tournament',
       'Date': 'date',
       'Series': 'series',
       'Court': 'court',
       'Surface': 'surface',
       'Round': 'round',
       'Best of': 'best_of',
       'Winner': 'player_1',
       'Loser': 'player_2',
       'WRank': 'player_1_rank',
       'LRank': 'player_2_rank',
       'WPts': 'player_1_points',
       'LPts': 'player_2_points',
       'W1': 'player_1_set_1',
       'L1': 'player_2_set_1',
       'W2': 'player_1_set_2',
       'L2': 'player_2_set_2',
       'W3': 'player_1_set_3',
       'L3': 'player_2_set_3',
       'W4': 'player_1_set_4',
       'L4': 'player_2_set_4',
       'W5': 'player_1_set_5',
       'L5': 'player_2_set_5',
       'Wsets': 'player_1_winner_sets',
       'Lsets': 'player_2_winner_sets',
       'Comment': 'comment',
       'B365W': 'player_1_bet365',
       'B365L': 'player_2_bet365',
       'PSW': 'player_1_pinnacle',
       'PSL': 'player_2_pinnacle',
       'MaxW': 'player_1_max',
       'MaxL': 'player_2_max',
       'AvgW': 'player_1_avg',
       'AvgL': 'player_2_avg'
   }

   return df.rename(columns=columns_new_names)

# Only grand slam series
def filter_grand_slam(df):
    filtered = df[df['series'] == 'Grand Slam']

    filtered.reset_index(drop=True, inplace=True)
    filtered.index = range(1, len(filtered) + 1)

    return filtered

def manage_nulls(df):
    df = df.apply(handle_nulls, axis=1, args=(df,))

    cols_to_check = [
        'tournament', 'surface', 'round', 
        'player_1', 'player_2',
        'player_1_bet365', 'player_2_bet365', 
        'player_1_pinnacle', 'player_2_pinnacle'
    ]
    df = df.dropna(subset=cols_to_check)

    return df

def handle_nulls(row, df):
    max_rank = df[['player_1_rank', 'player_2_rank']].max().max()
    if pd.isnull(row['player_1_rank']):
        row['player_1_rank'] = max_rank + 1
    elif pd.isnull(row['player_2_rank']):
        row['player_2_rank'] = max_rank + 1
    
    return row

def keep_columns(df):
    cols_to_keep = [
        'tournament', 'surface', 'round', 
        'player_1', 'player_2', 'player_1_rank', 'player_2_rank', 
        'player_1_bet365', 'player_2_bet365', 
        'player_1_pinnacle', 'player_2_pinnacle'
    ]

    return df[cols_to_keep]

def filter_test_df(train_df, test_df):
    player_names = set(train_df['player_1'].tolist() + train_df['player_2'].tolist())
    test_filtered = test_df[(test_df['player_1'].isin(player_names)) & (test_df['player_2'].isin(player_names))]

    return test_filtered

def add_winner_column(df):
    df['winner'] = 1
    return df

def swap_players(df):
    swap_rows = df.index[::2]

    df_swapped = df.loc[swap_rows]
    df_swapped['player_1'], df_swapped['player_2'] = df_swapped['player_2'], df_swapped['player_1']
    df_swapped['winner'] = 2

    for col in df.columns:
        if col.startswith('player_1_'):
            df_swapped[col], df_swapped[col.replace('player_1_', 'player_2_')] = df_swapped[col.replace('player_1_', 'player_2_')], df_swapped[col]

    df_new = pd.concat([df.loc[~df.index.isin(swap_rows)], df_swapped])
    return df_new

if __name__ == '__main__':
    csv_files = [f for f in os.listdir('./source/') if f.endswith('.csv')]
    for file_name in csv_files:
        df = pd.read_csv('./source/' + file_name)

        # rename columns
        renamed_df = rename_columns(df)

        filtered_df = filter_grand_slam(renamed_df) # hold only grand slam matches
        keeped_df = keep_columns(filtered_df) # keep only a few columns

        nullfree_df = manage_nulls(keeped_df)

        # add target column
        with_target_df = add_winner_column(nullfree_df)

        swapped_df = swap_players(with_target_df)

        swapped_df.to_csv('./output/modified_' + file_name, index=False)
    

    # post operations
    train_df = pd.read_csv('./output/modified_train_2023.csv')
    test_df = pd.read_csv('./output/modified_test_2024.csv')

    new_test = filter_test_df(train_df, test_df) # delete player from test that dont appear in train
    new_test.to_csv('./output/modified_test_2024.csv', index=False)