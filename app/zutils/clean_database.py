import pandas as pd

def datas():
    df = pd.read_csv("app/database/charts.csv")
    datas_unicas = df['date'].unique()
    datas_unicas_df = pd.DataFrame(datas_unicas, columns=['date'])
    datas_unicas_df['date'] = pd.to_datetime(datas_unicas_df['date'])
    datas_unicas_df = datas_unicas_df.sort_values(by='date')
    datas_unicas_df.to_csv('datas_unicas_ordenadas.csv', index=False)

import pandas as pd

def clean():
    df = pd.read_csv("app/database/charts.csv")
    
    df_filtered = df[["rank", "title", "date", "artist", "region", "streams"]].copy()

    df_filtered['date'] = pd.to_datetime(df_filtered['date'])

    df_filtered_2021 = df_filtered[df_filtered['date'].dt.year == 2021]

    df_country = df_filtered_2021[(df_filtered_2021["region"] == "Brazil") & (df_filtered_2021["rank"] <= 10)]

    df_country = df_country[df_country['streams'].notna() & (df_country['streams'] != '')]

    df_country_sorted = df_country.sort_values(by='date', ascending=True)

    df_country_sorted.to_csv('app/database/database_brazil.csv', index=False)


clean()