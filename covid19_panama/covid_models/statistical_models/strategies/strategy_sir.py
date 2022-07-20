from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset
import numpy


class SIRStrategy:
    parameters = {}
    training_data = None
    scaler = None
    model = None
    data = None
    forecast = None

    def compute_model(self):
        self.training_data = self.data[:-self.parameters['test_data_length']]
        test_data = self.data[-self.parameters['test_data_length']:]

        self.scaler = MinMaxScaler()
        self.scaler.fit(self.training_data)
        self.training_data = self.scaler.transform(self.training_data)
        test_data = self.scaler.transform(test_data)

        self.model = Sequential()
        self.training_data = self.data[:-61]
        self.scaler.fit(self.training_data)
        self.training_data = self.scaler.transform(self.training_data)

        n_input = self.parameters['test_data_length']
        self.parameters['number_of_features'] = len(self.data.columns)

        self.model.add(LSTM(50, return_sequences=True, input_shape=(n_input, self.parameters['number_of_features'])))
        self.model.add(LSTM(50))

        self.model.add(Dropout(0.10))
        self.model.add(Dense(self.parameters['number_of_features'], activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='mse')

        generator = TimeseriesGenerator(self.training_data, self.training_data, length=n_input, batch_size=25)

        self.model.fit_generator(generator, epochs=200)

    def generate_forecast(self):
        pred_list = []

        batch = (
            self.training_data[-self.parameters['test_data_length']:]
            .reshape(
                (
                    1,
                    self.parameters['test_data_length'],
                    self.parameters['number_of_features']
                )
            )
        )

        for i in range(self.parameters['test_data_length']):
            pred_list.append(self.model.predict(batch)[0])
            batch = numpy.append(batch[:, 1:], [[pred_list[i]]], axis=1)

        add_dates = [self.data.index[-1] + DateOffset(days=x) for x in range(0, self.parameters['test_data_length']+1)]
        future_dates = DataFrame(index=add_dates[1:], columns=self.data.columns)

        self.forecast = DataFrame(
            self.scaler.inverse_transform(pred_list),
            index=future_dates[-self.parameters['test_data_length']:].index,
            columns=[
                'Prediccion casos totales', 'Prediccion de nuevos casos', 'Predicciones defunciones totales',
                'Prediccion de Defunciones diarias', 'Prediccion de pruebas diarias', 'Prediccion Recuperados',
                'Prediccion recreativa', 'Prediccion supermercados', 'Prediccion parques',
                'Prediccion estaciones publicas', 'Prediccion trabajos', 'Prediccion residencial'
            ]
        )
