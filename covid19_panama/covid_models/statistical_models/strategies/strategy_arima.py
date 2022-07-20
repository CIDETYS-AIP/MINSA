class ARIMAStrategy:
    '''
    Criteria for models
    - AKAIKE criterion (could be easier)
    - Schawrz criterion

    Confidence interval of 5%

    NO-GO:
        - Based on parameters of moving average, auto-regression
    '''
    def get_validation_parameters(self):
        pass

    def set_validation_parameters(self, parameters):
        pass

    def retrieve_data(self):
        pass

    def compute_model(self, data):
        pass

    def validate_model(self, model, parameters):
        pass

    def generate_forecast(self, model):
        pass

    def store_results(self, results):
        pass

    def publish_results(self, results):
        pass
