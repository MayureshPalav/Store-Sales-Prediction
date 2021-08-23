import pandas as pd
from data_ingestion import data_loader
from data_processing import clean_data
from application_logging import logger
import pickle


class Preprocessing:

    def __init__(self):
        self.log_writer=logger.App_Logger()
        self.file_object=open('logs/processing.txt','a+')
    def cleaning_data(self):
        self.log_writer.log(self.file_object,'Processing_started')
        try:
            data_getter=data_loader.Data_Getter(self.file_object,self.log_writer)
            data=data_getter.get_data()
            """Processing"""
            preprocessor=clean_data.Preprocessor(self.file_object,self.log_writer)
            """Structuring our columns and Feature Engineering"""
            structured_data=preprocessor.structuring_columns(data)
            """Removing unwanted columns from the traning data"""
            cleaned_data = preprocessor.remove_columns(structured_data, 'Outlet_Establishment_Year')
            X, Y = preprocessor.separate_label_feature(cleaned_data, label_column_name="Item_Outlet_Sales")
            encoded_data, encoder = preprocessor.encodeCategoricalValues(X)
            "Save the encoder for later use "
            with open('Models/encoder.pickle', 'wb') as encoder_file:
                pickle.dump(encoder, encoder_file)
            """How many null values present for current training data"""
            nulls, cols_with_missing_values =preprocessor.is_null_present(encoded_data)
            """Check if we have missing data"""
            if (nulls):
                """If yes"""
                train_data = preprocessor.impute_missing_values(encoded_data)


            x_train,x_test,y_train,y_test=preprocessor.separating_train_test(train_data,Y)

            x_train_scaled,scaler_train=preprocessor.scale_numerical_columns(x_train)
            x_test_scaled,scaler_test=preprocessor.scale_numerical_columns((x_test))
            """We have our separate feature and target after cleaning the data"""
            with open('Models/scaler.pickle','wb') as encoder_file2:
                pickle.dump(scaler_train,encoder_file2)
            self.log_writer.log(self.file_object,'Done Preprocessing')
            self.file_object.close()
            return x_train_scaled, x_test_scaled, y_train, y_test
        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception