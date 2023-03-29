import pymongo
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from pymongo import MongoClient, DESCENDING
from datetime import datetime, timedelta
from bson.json_util import dumps

# connection string to connect to mongodb atlas
client = pymongo.MongoClient('mongodb+srv://lukewait:tafenosql@cluster1.syijvpg.mongodb.net/test')
# define db name
dbname = client['eduClimateAnalysis']
# define collection
climateDataCollection = dbname['climateData']
stationsCollection = dbname['stations']
usersCollection = dbname['users']

'''
# example url: http://localhost:8000/api/login/?username=user1&password=password1
def login(request):
    if request.method == 'GET':
        # Retrieve username and password from the GET request
        username = request.GET.get('username')
        password = request.GET.get('password')
        global client
        client = pymongo.MongoClient('mongodb+srv://lukewait:tafenosql@cluster1.syijvpg.mongodb.net/test')
        # Connect to MongoDB and query the "users" collection
        db = client['eduClimateAnalysis']
        users = db['users']
        user = users.find_one({'User Name': username, 'Password': password})

        if user:
            # Change the client connection based on the user's access level
            access_level = user['Access Level']
            
            if access_level == 'administrator':
                client = pymongo.MongoClient('mongodb+srv://administrator:tafenosql@cluster1.syijvpg.mongodb.net/test_admin')
            elif access_level == 'manager':
                client = pymongo.MongoClient('mongodb+srv://manager:tafenosql@cluster1.syijvpg.mongodb.net/test_manager')
            else:
                client = pymongo.MongoClient('mongodb+srv://user:tafenosql@cluster1.syijvpg.mongodb.net/test_user')
            
            return HttpResponse(f"<h1>Logged in as {access_level}</h1>")
        else:
            # Show an error message if the username/password combination is invalid
            error_message = 'Invalid username or password'
            return render(request, 'index', {'error_message': error_message})
    else:
        # Show the login form
        return render(request, 'index')
'''

# home page view
def index(request):
    return HttpResponse("<h1>Hello and welcome to the NoSQL Portfolio assignment")

# example url: http://localhost:8000/api/climateData/maxPrecipitation/
def maxPrecipitation(request):
    if request.method == "GET":
        try:
            # find the maximum precipitation value in the last 5 years
            startDate = datetime.now() - timedelta(days=5*365)
            maxPrecipitation = climateDataCollection.find_one(
                {'Time': {'$gte': startDate}},
                sort=[('Precipitation mm/h', DESCENDING)],
                projection={'_id': False, 'Precipitation mm/h': True}
            )
            # return the result as a JSON response
            return JsonResponse(maxPrecipitation, safe=False)

        except Exception as e:
            # Return a 500 error if there was an error processing the request
            return JsonResponse({'error': str(e)}, status=500)

# example url: http://localhost:8000/api/climateData/stationData/?device_id=dlb_atm41_5282&time=2021-05-05T21:44:05.000%2B00:00
def stationData(request):
    if(request.method == "GET"):
        try:
            # get the parameters from the query string
            deviceId = request.GET.get('device_id')
            timeStr = request.GET.get('time')
            # Convert the date string to a datetime object
            time = datetime.strptime(timeStr, '%Y-%m-%dT%H:%M:%S.%f+00:00')

            # Query the database for the specified device ID and time
            query = climateDataCollection.find_one({"Device ID": deviceId, "Time": time})

            if query is None:
                # Return a 404 error if the specified station or datetime could not be found
                return JsonResponse({"error": "Record not found."}, status=404)
            else:
                # Extract the desired fields from the resulting object
                temperature = query['Temperature (°C)']
                pressure = query['Atmospheric Pressure (kPa)']
                radiation = query['Solar Radiation (W/m2)']
                precipitation = query['Precipitation mm/h']

                # Return the results as a JSON object
                result = {
                    "Temperature (°C)": temperature,
                    "Atmospheric Pressure (kPa)": pressure,
                    "Solar Radiation (W/m2)": radiation,
                    "Precipitation mm/h": precipitation
                }
                return JsonResponse(result, safe=False)

        except ValueError as e:
            # Return a 400 error if the query string is invalid
            return JsonResponse({"error": "Invalid query string: {}".format(str(e))}, status=400)

        except Exception as e:
            # Return a 500 error if an unexpected exception occurs
            return JsonResponse({"error": str(e)}, status=500)
        
# example url: http://localhost:8000/users/
def users(request):
    # example request body:
    # {
    # "Access Level": "manager",
    # "Name": "guy",
    # "Password": "qwerty",
    # "User Name": "new user"
    # }
    if request.method == "POST":
        try:
            # get the current time to input as Last Login
            currentTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
            lastLogin = datetime.strptime(currentTime, '%Y-%m-%dT%H:%M:%S.%f+00:00')

            # validate input
            # required_fields = ['Access Level', 'Name', 'Password', 'User Name']
            # for field in required_fields:
            #     if field not in body:
            #         raise ValueError(f"Missing required field: {field}")
                
            # TODO: input validation, e.g. password strength, username uniqueness

            # read the body contents and insert into mongodb collection
            body = json.loads(request.body.decode("utf-8"))
            newUser = {
                "Access Level": body['Access Level'],
                "Last Login": lastLogin,
                "Name": body['Name'],
                "Password": body['Password'],
                "User Name": body['User Name']
            }
            result = usersCollection.insert_one(newUser)
            data = {"_id": str(result.inserted_id)}
            return JsonResponse(data, safe=False)
    
        except ValueError as e:
            # Return a 400 error if there was a problem with the request body
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            # Return a 500 error if there was an error processing the request
            return JsonResponse({'error': str(e)}, status=500)
        
    # if(request.method == "DELETE"):
        # todo
        # single and multiple (maybe use query string to determine)