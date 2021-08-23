import pandas as pd

class Data_Getter:
    """
    To get data from the source
    """
    def __init__(self, file_object, logger_object):
        self.training_file='data_files/Train.csv'
        self.file_object=file_object
        self.logger_object=logger_object

    def get_data(self):
        """
        This method reads the data from source A pandas DataFrame.
        """
        self.logger_object.log(self.file_object,'Getting data ')
        try:
            self.data= pd.read_csv(self.training_file) # reading the data file
            self.logger_object.log(self.file_object,'Loaded data successfully')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception has occured in data get_data method '+str(e))
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()


