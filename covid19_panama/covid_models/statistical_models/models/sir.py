from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
import io
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import warnings
warnings.filterwarnings("ignore")

# Bases de datos
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
data = requests.get(url).content
paises = pd.read_csv(io.StringIO(data.decode()), parse_dates=True, squeeze=True)
panama = paises.loc[paises['location'] == "Panama"]
panama = panama.fillna(0)
panama.date = pd.to_datetime(panama.date)
panama.index = pd.to_datetime(panama.date)
panama = panama[:357]

data3 = requests.get(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv").content
paises_recu = pd.read_csv(io.StringIO(data3.decode()), parse_dates=True, squeeze=True)
panama_recu = paises_recu.loc[paises_recu['Country/Region'] == "Panama"]
panama_recu = panama_recu.drop(['Province/State', 'Lat', 'Long'], axis=1)
panama_recu = panama_recu.T
panama_recu.columns = ['recuperados']
panama_recu = panama_recu[48:405]
panama_recu = panama_recu.apply(pd.to_numeric)

panama2 = panama.set_index('date')
panama2 = panama[['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'new_tests']]
panama2.rename({'': 'total_cases'}, inplace=True)
panama2.columns = ['casos_totales', 'nuevos_casos', 'defunciones_totales', 'defunciones_nuevas', 'nuevas_pruebas']
panama2 = panama2.asfreq(freq='1D')
# panama2=panama2[46:283]

mobilidad = pd.read_csv(
    r"C:\Users\Jaime\Documents\UTP\X SEMESTRE\TRABAJO DE GRADUACION\PROYECTO COVID\DATA FINAL\2020_PA_Region_Mobility_Report.csv", parse_dates=True, squeeze=True)
mobilidad.index = pd.to_datetime(mobilidad.date)
mobilidad = mobilidad[['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline',
                       'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline']]
mobilidad = mobilidad[23:380]

# Concatenando la data de recuperados y las de mobilidad
panama2 = pd.concat([panama2, panama_recu], axis=1)
panama2 = pd.concat([panama2, mobilidad], axis=1)
# panama2.isnull().any().any()
panama2.tail(5)

# Dividiendo los datos en los grupos para entrenamiento y prueba
test_lenght = 0.1*len(panama2.index)
test_lenght = math.ceil(test_lenght)
train, test = panama2[:-test_lenght], panama2[-test_lenght:]

# Escalando y transformando los datos
scaler = MinMaxScaler()
scaler.fit(train)
train = scaler.transform(train)
test = scaler.transform(test)

n_input = test_lenght
n_features = len(panama2.columns)

generator = TimeseriesGenerator(train, train, length=n_input, batch_size=25)

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(n_input, n_features)))
# model.add(LSTM(100, return_sequences=True))
model.add(LSTM(50))

model.add(Dropout(0.10))
model.add(Dense(n_features, activation='sigmoid'))
model.compile(optimizer='adam', loss='mse')

history = model.fit_generator(generator, epochs=400)
model.summary()
pred_list = []

first_eval_batch = train[-n_input:]

current_batch = first_eval_batch.reshape(1, n_input, n_features)


for i in range(n_input):
  pred_list.append(model.predict(current_batch)[0])
  current_batch = np.append(current_batch[:, 1:, :], [[pred_list[i]]], axis=1)

panama2_predict = pd.DataFrame(scaler.inverse_transform(pred_list), index=panama2[-n_input:].index, columns=['Prediccion casos totales', 'Prediccion de nuevos casos', 'Predicciones defunciones totales', 'Prediccion de Defunciones diarias',
                               'Prediccion de pruebas diarias', 'Prediccion Recuperados', 'Prediccion recreativa', 'Prediccion supermercados', 'Prediccion parques', 'Prediccion estaciones publicas', 'Prediccion trabajos', 'Prediccion residencial'])
panama2_test = pd.concat([panama2, panama2_predict], axis=1)
panama2_test.tail()

fig, axs = plt.subplots(3, 2, figsize=(20, 15), sharex=True)

# plt.figure(figsize=(15,10))
axs[0, 0].plot(panama2.index, panama2_test.iloc[:, 0], label='Prediccion de casos ')
axs[0, 0].plot(panama2.index, panama2_test.iloc[:, 12], label='Datos historicos')
axs[0, 0].set_title('Casos totales')
axs[0, 1].plot(panama2.index, panama2_test.iloc[:, 1], label='Prediccion de casos ')
axs[0, 1].plot(panama2.index, panama2_test.iloc[:, 13], label='Datos historicos')
axs[0, 1].set_title('Casos nuevos')
axs[1, 0].plot(panama2.index, panama2_test.iloc[:, 2], label='Prediccion de casos ')
axs[1, 0].plot(panama2.index, panama2_test.iloc[:, 14], label='Datos historicos')
axs[1, 0].set_title('Total defunciones')
axs[1, 1].plot(panama2.index, panama2_test.iloc[:, 3], label='Prediccion de casos ')
axs[1, 1].plot(panama2.index, panama2_test.iloc[:, 15], label='Datos historicos')
axs[1, 1].set_title('Defunciones nuevas')
axs[2, 0].plot(panama2.index, panama2_test.iloc[:, 4], label='Prediccion de casos ')
axs[2, 0].plot(panama2.index, panama2_test.iloc[:, 16], label='Datos historicos')
axs[2, 0].set_title('Nuevas pruebas')
axs[2, 1].plot(panama2.index, panama2_test.iloc[:, 5], label='Prediccion de casos ')
axs[2, 1].plot(panama2.index, panama2_test.iloc[:, 17], label='Datos historicos')
axs[2, 1].set_title('Recuperados')
for row in axs:
    for ax in row:
        ax.grid(b=True, which='major', color='#666666', linestyle='-')
        ax.minorticks_on()
        ax.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Entrenamiento')
# plt.plot(history.history['val_loss'],label='Validacion')
plt.legend()
plt.grid()
plt.show()

# RMSE Erro para nuevos casos
rmse_rs = []
for i in range(6):
    rmse_rs.append(sqrt(mean_squared_error(panama2_test.iloc[333:, i].values, panama2_test.iloc[333:, i+12].values)))

print(rmse_rs)
train = panama2[:-61]
scaler.fit(train)
train = scaler.transform(train)


n_input = test_lenght
n_features = len(panama2.columns)

generator = TimeseriesGenerator(train, train, length=n_input, batch_size=25)

history2 = model.fit_generator(generator, epochs=200)

pred_list = []

batch = train[-n_input:].reshape((1, n_input, n_features))

for i in range(n_input):
    pred_list.append(model.predict(batch)[0])
    batch = np.append(batch[:, 1:], [[pred_list[i]]], axis=1)

plt.figure(figsize=(10, 5))
plt.plot(history2.history['loss'], label='Prediccion')
plt.xlabel("Iteracion")
plt.ylabel("Perdida")
plt.title('Perdida en los valores de la prediccion')
plt.legend()
plt.grid()
plt.show()

add_dates = [panama2.index[-1] + DateOffset(days=x) for x in range(0, test_lenght+1)]
future_dates = pd.DataFrame(index=add_dates[1:], columns=panama2.columns)

panama2_predict = pd.DataFrame(scaler.inverse_transform(pred_list), index=future_dates[-n_input:].index, columns=['Prediccion casos totales', 'Prediccion de nuevos casos', 'Predicciones defunciones totales', 'Prediccion de Defunciones diarias',
                               'Prediccion de pruebas diarias', 'Prediccion Recuperados', 'Prediccion recreativa', 'Prediccion supermercados', 'Prediccion parques', 'Prediccion estaciones publicas', 'Prediccion trabajos', 'Prediccion residencial'])
panama2_proj = pd.concat([panama2, panama2_predict], axis=1)
panama2_proj.iloc[357:, 12:18].head(31)
