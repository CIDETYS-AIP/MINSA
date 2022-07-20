import logging
logger = logging.getLogger(__name__)


class CSVStrategy:
    files = []
    callbacks = []
    dataframe_start_end = []
    read_file_functions = []
    cleaned_data = {}
    consolidate_data_function = None

    def __init__(
        self,
        files,
        callbacks,
        read_file_functions,
        consolidate_data_function,
        dataframe_start_end,
        *args, **kwargs
    ):
        self.files = files
        self.callbacks = callbacks
        self.read_file_functions = read_file_functions
        self.consolidate_data_function = consolidate_data_function
        self.dataframe_start_end = dataframe_start_end

    def clean(self):
        assert len(self.dataframe_start_end) == len(self.callbacks)
        assert len(self.files) == len(self.callbacks)
        assert len(self.read_file_functions) == len(self.files)

        for index, callback in enumerate(self.callbacks):
            cleaning_parameters = {
                'file': self.files[index],
                'callback': callback,
                'read_file_function': self.read_file_functions[index],
                'consolidate_data_function': self.consolidate_data_function,
                'dataframe_start_end': self.dataframe_start_end[index],
            }

            logger.info(f'Cleaning parameters: {cleaning_parameters}')

            dataframe = self.read_file_functions[index](self.files[index])
            key, value = callback(
                dataframe,
                start=self.dataframe_start_end[index]['start'],
                end=self.dataframe_start_end[index]['end']
            )
            self.cleaned_data[key] = value

        self.cleaned_data = self.consolidate_data_function(self.cleaned_data)

        return self.cleaned_data
