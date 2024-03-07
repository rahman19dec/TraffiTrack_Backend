This backend is developed for TraffiTrack system which is planned to deploy on Jetson Nano Developer Kit.

If you want to run on a different system for example on your laptop, some python dependencies might be irrelevent.
Create a python3 environent (python 3.8+) and activate it.

run the main.py file to run the program, and you have to run the fapi/app.py to make the apis available.
both can be run from the work directory.

## API access points

### /all

returns all result from the database in array format

### /classes

returns a json map of class names and class ids

### /count (optional: from_time, to_time)

returns counts of objects in a json dictionary. if no from_time or to_time arguemnts are given, returns count of all time <br>
Examples:
<br>http://localhost:5000/count
<br>http://localhost:5000/count?from_time=2024-02-24T13:00:00
<br>http://localhost:5000/count?from_time=2024-02-24T12:00:00&to_time=2024-02-24T13:00:00

### /carbon (optional: from_time, to_time)<br>
returns carbon estimte for both individual classses and total emission<br>
<br>note that here 'T' is used to seperate date and time, you can leave a space, or %20

### /stat (optional: from_time, to_time)

returns number of object instances by time. 
<br> Example:
<br>http://localhost:5000/stat?from_time=2024-02-24T12:00:00&to_time=2024-02-24T13:00:00
