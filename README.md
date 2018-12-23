# Detect-Parkinson-s
Our Android app named Detect Parkinson's is used to detect Parkinson's Disease.Our Android app is based on Navigation Drawer Activity.User's details will be stored in SQLite Database.SQLite Database is used to store details offline. SQLite lets you store data in structured manner.This application file is portable across all operating systems, 32-bit and 64-bit and big- and little-endian architectures.Content can be accessed and updated using powerful SQL queries, greatly reducing the complexity of the application code.Our Homepage works on WebView.A WebView is a view that displays web content right inside your app.


The “Detect Parkinson’s” mobile application is connected with the live website that processes the features of Parkinson’s disease. The website is developed using pyramid framework which uses ORM model (SQLalchemy) . Thus security of the user’s data is maintained. The website analyses the features of Parkinson’s disease that is the image and speech. The website is currently not deployed in AWS, you can run the website using the command “pserve development.ini” .
Requirements to run the website – create a virtual environment in python3.6 and install pyramid, pandas , numpy ,seaborn ,bokeh,matplotlib.

The speech features(around 754 features with 2 classes) are classified using random forest algorithm.
Requirements to run “new_data_prediction_final.py” file – create a virtual environment in python3.6 and install sklearn, pandas.
The dataset(“pd_speech_features.csv”) needed to run “new_data_prediction_final.py” is attached in the parkinson folder.
