import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from category_encoders import OrdinalEncoder
from sklearn.model_selection import train_test_split


class Preprocessor:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self,data,columns):



        self.logger_object.log(self.file_object, 'Removing columns')
        self.data=data
        self.columns=columns
        try:
            self.useful_data=self.data.drop(labels=self.columns, axis=1) # drop the labels specified in the columns
            self.logger_object.log(self.file_object,
                                   'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in remove_columns method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                                   'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        """

                     This method separates the features and a Label Coulmns.


                """
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X=data.drop(labels=label_column_name,axis=1) # drop the columns specified and separate the feature columns
            self.Y=data[label_column_name] # Filter the Label columns
            self.logger_object.log(self.file_object,
                                   'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X,self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def structuring_columns(self,data):
        """Here we deal with inconsistent values in our datasets which we found  their are some columns with inconsistency also feature engineering
        """
        self.logger_object.log(self.file_object,'Entered structuring_columns method of the Preprocessor class')
        try:
            data['Item_Fat_Content'].replace('reg', 'Regular',inplace=True)
            data['Item_Fat_Content'].replace(['low fat', 'LF'], 'Low Fat',inplace=True)

            data['Item_Identifier'] = data['Item_Identifier'].apply(lambda x: x[:-2])
            data['Item_Visibility'].replace(0, np.nan, inplace=True)
            data['Outlet_Size'].fillna('Small',inplace=True)
            "We will bin the year column into three parts"
            label = ['Before 1984', 'Between 1984 & 1999', 'After 1999']
            data['Year'] = pd.qcut(data['Outlet_Establishment_Year'], q=[0, 0.19, 0.50, 1.0], labels=label)
            data['Year']=data['Year'].astype(object)

            return data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate cleaning_nans_preprocessing of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'cleaning_nans_preprocessing Unsuccessful. Exited  the Preprocessor class')
            raise Exception()



    def is_null_present(self,data):
        """

                               Will return number of null values in ecah columns


                        """
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.cols_with_missing_values=[]
        self.cols = data.columns
        try:
            self.null_counts=data.isna().sum() # check for the count of null values per column
            for i in range(len(self.null_counts)):
                if self.null_counts[i]>0:
                    self.null_present=True
                    self.cols_with_missing_values.append(self.cols[i])
            if(self.null_present): # write the logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = data.columns
                self.dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            self.logger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()

    def encodeCategoricalValues(self,data):
     """
                                        Encoding Categorical features"""

     self.logger_object.log(self.file_object,'Encoding categorical features')
     self.data=data
     self.data.to_csv('encoder_d.csv',index=False)
     cats = [cols for cols in self.data.columns if self.data[cols].dtypes == 'O']
     # create ordinal encode object
     ordinal_encoder = OrdinalEncoder(cols=cats,return_df=True,
                                      handle_unknown="error")

     # fit object on the train dataset
     ordinal_encoder.fit(self.data)
     data=ordinal_encoder.transform(self.data)
     data.to_csv('encoded_data.csv',index=False)


     return data,ordinal_encoder

    def scale_numerical_columns(self,data):

        self.logger_object.log(self.file_object,
                               'Entered the scale_numerical_columns method of the Preprocessor class')

        self.data=data
        nums=['Item_Weight', 'Item_Visibility', 'Item_MRP']

        try:

            self.scaler = MinMaxScaler()
            self.data[nums]= self.scaler.fit_transform(self.data[nums])
            self.logger_object.log(self.file_object, 'scaling for numerical values successful. Exited the scale_numerical_columns method of the Preprocessor class')
            return self.data,self.scaler
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in scale_numerical_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'scaling for numerical columns Failed. Exited the scale_numerical_columns method of the Preprocessor class')
            raise Exception()


    def impute_missing_values(self, data):
        """Description: This method replaces all the missing values in the Dataframe using KNN Imputer."""
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data= data
        try:
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            self.new_data=pd.DataFrame(data=(self.new_array), columns=self.data.columns)
            self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def separating_train_test(self, feature, target):
        self.logger_object.log(self.file_object, "Separating train and test")
        try:

            x_train, x_test, y_train, y_test = train_test_split(feature, target, test_size=0.30)
            self.logger_object.log(self.file_object,
                               'Done separating train and test')

            return x_train, x_test, y_train, y_test
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separating train and test' + str(e))
            raise Exception()
