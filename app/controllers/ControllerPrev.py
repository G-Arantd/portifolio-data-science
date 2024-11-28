from app.controllers.ControllerDatabase import *

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd

def prev_top_artist():
    df_monthly_2017 = get_data_analysis(2017)
    df_monthly_2018 = get_data_analysis(2018)
    df_monthly_2019 = get_data_analysis(2019)
    df_monthly_2020 = get_data_analysis(2020)

    df_monthly_full = pd.concat([df_monthly_2017, df_monthly_2018, df_monthly_2019, df_monthly_2020])

    df_monthly_full['date'] = pd.to_datetime(df_monthly_full['month'], format='%Y-%m')
    df_monthly_full['year'] = df_monthly_full['date'].dt.year
    df_monthly_full['month'] = df_monthly_full['date'].dt.month
    df_monthly_full['quarter'] = df_monthly_full['date'].dt.quarter

    df_monthly_full['monthly_rank'] = df_monthly_full.groupby('month')['total_streams'].rank(
        method='dense', ascending=False
    )

    rank_annual = (
        df_monthly_full.groupby(['artist', 'year'], as_index=False)['total_streams']
        .sum()
        .assign(annual_rank=lambda x: x.groupby('year')['total_streams'].rank(
            method='dense', ascending=False
        ))
    )
    df_monthly_full = pd.merge(
        df_monthly_full, rank_annual[['artist', 'year', 'annual_rank']],
        on=['artist', 'year'], how='left'
    )

    artist_month_streams = df_monthly_full.groupby(['artist', 'year'])['total_streams'].sum().reset_index()
    artist_month_streams['rolling_mean'] = artist_month_streams.groupby('artist')['total_streams'].transform(
        lambda x: x.rolling(window=6, min_periods=1).mean()
    )
    artist_month_streams['streams_growth'] = artist_month_streams.groupby('artist')['total_streams'].pct_change().fillna(0)

    artist_month_streams = pd.merge(
        artist_month_streams, rank_annual[['artist', 'year', 'annual_rank']],
        on=['artist', 'year'], how='left'
    )

    train_data = artist_month_streams[artist_month_streams['year'] <= 2020]
    test_data = artist_month_streams[artist_month_streams['year'] == 2020]

    X_train = train_data[['year', 'streams_growth', 'rolling_mean', 'annual_rank']]
    y_train = train_data['total_streams']
    X_test = test_data[['year', 'streams_growth', 'rolling_mean', 'annual_rank']]
    y_test = test_data['total_streams']

    model = RandomForestRegressor(
        n_estimators=9, 
        max_depth=50,
        random_state=42,
        min_samples_leaf=1,
        min_samples_split=3
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    test_data = test_data.assign(predicted_streams=y_pred)

    top_10_artists = test_data.sort_values(by='predicted_streams', ascending=False).head(10)
    result = top_10_artists[['artist', 'predicted_streams']]

    print(f"MAE (Erro Médio Absoluto): {mae}")
    print(f"R² (Coeficiente de Determinação): {r2}")

    json_result = result.to_dict(orient='records')
    return json_result