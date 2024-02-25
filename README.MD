## API access points

### /all

returns all result from the database in array format

### /classes

returns a json map of class names and class ids

### /count (optional: from_time, to_time)

return counts of objects in a json dictionary. if no from_time or to_time arguemnts are given, returns count of all time
Examples:
http://localhost:5000/count
http://localhost:5000/count?from_time=2024-02-24T13:00:00
http://localhost:5000/count?from_time=2024-02-24T12:00:00&to_time=2024-02-24T13:00:00
note that here 'T' is used to seperate date and time, you can leave a space, or %20
