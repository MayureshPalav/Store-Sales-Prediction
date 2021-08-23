from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from application_logging import logger



class Connector:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open('logs/Database.txt', 'a+')
        self.Client_id = 'TKzcQZLcRbghabrspOCcIkmo'
        self.Client_secret = 'RH7OOpfPxHRiIF5gAr-lRRGbrgejdbyjgCU5i++wzZWZ13RIW8mlw4X_d-.r01bSSs5JyKW6vrga+1CZadNbd2NMlDv31-x3DO5IclRPyegLvJgu195inuT_+1PWCi66'
        cloud_config = {'secure_connect_bundle': 'secure-connect-food-price-prediction.zip'}
        auth_provider = PlainTextAuthProvider(self.Client_id, self.Client_secret)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        #cluster = Cluster(['127.0.0.1'], port=9042)
        self.session = cluster.connect()
        self.log_writer.log(self.file_object,"Connected to Database")

    def master(self):
        """
        Creates table if not existed into database

        """
        self.session.execute("USE store")
        self.session.execute("select release_version from system.local")
        self.session.execute("CREATE TABLE store_sales_2(Item_Identifier text,Item_Weight int,Item_Fat_Content text,Item_Visibility float,Item_Type text,Item_MRP int,Outlet_Identifier text,Outlet_Size text,Outlet_Location_Type text,Outlet_Type text,Year text,id uuid PRIMARY KEY);")
        self.log_writer.log(self.file_object,"Succesfully created table ")
    def addData(self, result):
        """
        Gets data from user and puts it into database

        """


        columns = "Item_Identifier,Item_Weight,Item_Fat_Content,Item_Visibility,Item_Type,Item_MRP,Outlet_Identifier,Outlet_Size,Outlet_Location_Type,Outlet_Type,Year,id"
        self.log_writer.log(self.file_object, "Created Column Names ")
        value = "'{0}',{1},'{2}',{3},'{4}',{5},'{6}','{7}','{8}','{9}','{10}',{11}".format(result['Item_Identifier'][0], result['Item_Weight'][0], result['Item_Fat_Content'][0],
                                                                 result['Item_Visibility'][0], result['Item_Type'][0],
                                                                 result['Item_MRP'][0], result['Outlet_Identifier'][0],
                                                                 result['Outlet_Size'][0],result['Outlet_Location_Type'][0],
                                                                 result['Outlet_Type'][0],result['Year'],'uuid()')
        self.log_writer.log(self.file_object, "Prepared Values to add in Database")

        custom = "INSERT INTO store_sales_2({}) VALUES({});".format(columns, value)


        self.session.execute("USE store")

        output = self.session.execute(custom)

        self.log_writer.log(self.file_object, "Succesfully added Data into Database Table ")




    def getData(self):
        """
         Retrieves Data from Database
        """
        self.session.execute("USE store")
        row = self.session.execute("SELECT * FROM Prediction_updated;")
        collection = []
        for i in row:
            collection.append(tuple(i))
        return tuple(collection)
