import pandas as pd

def clean():
    df = pd.read_csv("charts.csv")
    
    df_filtered = df[["title", "rank", "date", "artist", "region", "streams"]].copy()
    
    df_filtered['date'] = pd.to_datetime(df_filtered['date'])
    
    df_country = df_filtered[(df_filtered["region"] == "Brazil") & (df_filtered["rank"] <= 50)]
    
    df_country = df_country[df_country['streams'].notna() & (df_country['streams'] != '')]
    
    df_country_sorted = df_country.sort_values(by='date', ascending=True)
    
    df_country_sorted = df_country_sorted.drop(columns='rank')
    
    df_country_sorted.to_csv('database_brazil.csv', index=False)

def view_data():
    df = pd.read_csv("charts.csv")
    
    print(df.columns)

clean()

# def datas():
#     df = pd.read_csv("app/database/charts.csv")
#     datas_unicas = df['date'].unique()
#     datas_unicas_df = pd.DataFrame(datas_unicas, columns=['date'])
#     datas_unicas_df['date'] = pd.to_datetime(datas_unicas_df['date'])
#     datas_unicas_df = datas_unicas_df.sort_values(by='date')
#     datas_unicas_df.to_csv('datas_unicas_ordenadas.csv', index=False)