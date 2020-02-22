# IU-Witcher-2020

## Team members
- Vishal Patel
- Sanyam Rajpal
- Akshay Gupta

## Installation instructions:
[Wiki page](https://github.com/airavata-courses/IU-Witcher-2020/wiki/Project-1)

## Languages used
* PHP - User Management
* Python - Data Retrieval, Model Execution, Post Processing and API Gateway
* Javascript - User Interface, Session Management, NoSql Database

## Messenger
RabbitMQ is used as the only source of communication for interaction within the microservices as well for the interaction of microservices with the API Gateway. It requires elements that will be pushed and popped from the queue to be JSON objects.

## Microservices
The connection is established using the Pika library to the RabbitMQ server. All the queues will be initialized in both the sender and the receiver of the queue.
Not all the microservices and the API gateway act both as sender and receiver of some information. Since in RabbitMQ the concept is such that the receiver keeps on running and consumes whenever something is pushed in by the sender so it runs indefinitely until interrupted. So to keep all the services running one has to add an infinite loop to keep the code running until manually interrupted. Since not all the queues pass on data at the same speed there will be some queues which will end up getting stacked at a pace more than its elements are extracted.

### Data Retrieval
Data Retrieval receives user location from the API Gateway. Then it downloads a temporary file locally from the Nexrad AWS directory. The file downloaded from the NEXRAD AWS directory is of the time closest to the current time since the current time data isn't available in the directory. In this as an error handling step, we take the second last file updated in the directory to handle the case let's say the last directory is in the process of being uploaded and it is called at that instance by the microservice. It may throw an error if say the file is incomplete. So to handle that we have considered the second last file in the directory and hence the last reliable complete directory because only if that file's update is complete will the uploading of the next file start. Since the data can be accessed as class Object it can't be passed on in the Queue of RabbitMQ. It can't be converted to a JSON object while not losing any of its methods and properties. So we extract the information in lists which can be accessed as values in the dictionary which will be passed on as a JSON object. The previous object having user details is merged with the current data extracted from the class object to be sent to the Model Execution.
* For now the data retrieval works fine for every time period except when one calls the code sharp at midnight when the new directory doesn't have any complete file and has 1 file in the process of being uploaded. In such case, the code might malfunction but doesn't necessarily always do. Its very unlikely yet not impossible to be disregarded.
* The current code works for the current time zone from where the code is running. If the time zone is behind the Greenwich Mean Time then it doesn't have any problem accessing the file since it tries to access time before the greenwich time but if it tries to access a date which hasn't actually happened in the Greenwich so it will have to be adjusted to the current date and time for greenwich but for all the places behind the greenwich this isn't a problem like the USA.

### Model Execution
Model Execution receives user location and the latest weather data from Data Retrieval. Model execution calls the OpenWeatherMap API to get the forecasting data by using the USER location. Since the API gives plenty of parameters, some of the less important parameters are filtered. Then the parameters are converted is merged into a JSON object with the previous data. Note every time we merge data to the JSON object, there might be a hierarchy of dictionary for every merge. So if let's say we have 10 microservices, we have to access the dictionary[ "Key1" ][ "Key2" ]...[ "Key10" ] which will be really cumbersome. So we make sure that the elements of the dictionary are merged not the dictionary as a whole.

### Post Processing
In post-processing, we get use the weather data to plot the range of Reflectivity for the most recently updated data in AWS Nexrad Directory for the current date. After generating an image for the same we save it locally. Then we add the image to a bucket in the AWS directory and make it public. Then we pass on the predesignated URL along with the forecasting data to the API Gateway using RabbitMQ which will eventually be shown to the USER.

### Session Management
The Session Manager is responsible for 2 tasks. One, it saves all the queries that the user has made on the Front-end. Two, it allows the user to access these queries later. It creates an interaction with the Front-end through the API-Gateway. The Session Manager is built as a `Node.js` server using the `Express.js` framework. It uses a local instance of `MongoDB` for saving the user related data.

## References
* [AWS]( https://www.nsstc.uah.edu/users/brian.freitag/AWS_Radar_with_Python.html )
* [RabbitMQ]( https://www.rabbitmq.com/tutorials/tutorial-one-python.html )
* [Nexrad]( https://unidata.github.io/python-gallery/examples/Nexrad_S3_Demo.html )
* [Metpy]( https://unidata.github.io/MetPy/latest/examples/formats/NEXRAD_Level_2_File.html )
* [AWS Bucket]( https://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto )
