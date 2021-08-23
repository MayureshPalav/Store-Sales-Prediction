
# Store Sales Predictions

Store sales prediction aims at accurately predicting sales of particular items based on features like weight,price and also location at which it is been sold like a supermarket or a retail shop.This software system will be a Web application.This can be used by the warehouse management to forecast the sales for each of their items and take business decision accordingly 


## Steps taken to deliver end-to-end product

1. Performing EDA on the dataset to first understand every aspect of it.

2. Start designing the pipeline which will automate the process of data cleaning,data preprocessing,feature engineering,feature selection,transformation and scaling.

3. Once ready we perform train and test split and feed the training data to 3 separate models.

4. Using Gridsearchcv we get best model evaluated on our test set and we save that model.

5. This process is designed a pipeline and can be retrained anytime with necessary changes.

6. This model is using Flask API and is deployed on AWS EC2 & HEROKU.

7. User queries are stored within cassandra Nosql database which can be used later for retraining.

8. Logs are maintained in separate files for training and database operations

  
## Deployment

Heroku:  https://store-sales.herokuapp.com

AWS EC2 : ec2-3-144-36-208.us-east-2.compute.amazonaws.com:8080/



  
## User interface for store sales prediction

![homepage_final](https://user-images.githubusercontent.com/54542692/130473549-615f99ec-b85f-45e2-8f3b-43c6bde90f75.png)


ABOUT SECTION

![about](https://user-images.githubusercontent.com/54542692/130473639-2bf5669d-782e-4273-abb9-3e67e13a97b2.png)


User needs to fill this form to get forecast sales of items he/she mentions

![form](https://user-images.githubusercontent.com/54542692/130473661-2ae1b0aa-5f7a-484b-a4f4-1670d351f0d3.png)


After clicking  submit button user gets the info passed along with forecasted sales and average sales of that product accross all units

![congrats_results](https://user-images.githubusercontent.com/54542692/130473831-29db4d0b-278e-447c-8d43-7e835dc8f465.png)

Features affecting sales of the product

![factors](https://user-images.githubusercontent.com/54542692/130473904-b3823d47-6eae-4227-aa23-026cef8368da.png)


![Annotation 2021-08-18 182336](https://user-images.githubusercontent.com/54542692/129901549-50b82d6a-20e6-46cb-a6bf-f12619f81970.png)

Logging done during training Pipeline

![Annotation 2021-08-18 182512](https://user-images.githubusercontent.com/54542692/129901725-35d7c7e4-26ce-41f9-b03f-d0c48640ad3b.png)







Tools used 
- Pandas,Numpy,seaborn
- Python
- FLASK
- Sklearn
- logging
- Cassandra NoSql Database
- AWS
- HEROKU
