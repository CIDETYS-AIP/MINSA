from .statistical_model import StatisticalModel


class ARIMAModel(StatisticalModel):
    '''
    General algorithm
    1. Obtain data from excel sheet in github repo.
    2. Create new cases per day graph.
    3. Determine mean of distribution.
    4.

    '''
    def retrieve_data(self, url='', file_type='excel'):
        data = {}
        if file_type == 'excel':
            pass
        return data

    def store_data(self):
        pass

    def compute(self):
        pass

    def validate(self, model, validation_params={}):
        '''
        must be more than t_value

        Bob-Jenkins methodology for validation

        validation_params = {
            't_value': 2,
            'chi_squared': 0.0,
            'ms_error': 0.0
        }
        '''
        is_valid = False
        if validation_params:
            pass
        return is_valid

    def forecast(self, iterations=0):
        pass

    def store_result(self):
        pass

    def publish(self):
        pass

    def create_graph_new_cases_per_date(self, excel_sheet, date_config):
        '''
        date_config = {
            "start_date": "",
            "end_date": ""
        }
        '''
        pass

    def create_differentiation_graph(self, data):
        pass

    def create_correlation_graph(self, data):
        pass

    def series_is_stationary(self, series):
        pass

    def series_is_temporal(self, series):
        pass
