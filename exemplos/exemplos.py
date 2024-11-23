import pandas as pd

def clean():
    df = pd.read_csv("charts.csv")
    selected_columns = df[["title", "rank", "date", "artist", "region", "streams"]].copy()
    selected_columns['date'] = pd.to_datetime(selected_columns['date'])
    target_countries = ['Brazil', 'Argentina', 'Mexico', 'Uruguay']
    filtered_df = selected_columns[(selected_columns["region"].isin(target_countries)) & (selected_columns["rank"] <= 200)]
    filtered_df = filtered_df[filtered_df['streams'].notna() & (filtered_df['streams'] != '')]
    sorted_df = filtered_df.sort_values(by='date', ascending=True)
    sorted_df = sorted_df.drop(columns='rank')
    sorted_df.to_csv('instance/csv/data.csv', index=False)

clean()

# def view_data():
#     df = pd.read_csv("charts.csv")
    
#     print(df.columns)

# def datas():
#     df = pd.read_csv("app/database/charts.csv")
#     datas_unicas = df['date'].unique()
#     datas_unicas_df = pd.DataFrame(datas_unicas, columns=['date'])
#     datas_unicas_df['date'] = pd.to_datetime(datas_unicas_df['date'])
#     datas_unicas_df = datas_unicas_df.sort_values(by='date')
#     datas_unicas_df.to_csv('datas_unicas_ordenadas.csv', index=False)