import requests
import csv
import json

# configuration values
config = dict(
    username="<cloudant_account>", 
    password="<cloudant_password>",
    database="<cloudant_database>")

# dict of table names and their csv representations
csv_lookup = {
    # "table_name": "path/to/file.csv"
    "<table_name>": "<csv_file_name>.csv"
}

# dict of request data, which we'll upload to Cloudant
requests_data = {}

for table, filepath in csv_lookup.iteritems():
    request_data = dict(docs=[]) 
    # get our data
    with open(filepath, 'rb') as f:
        reader = csv.DictReader(f)
        # put into request body    
        for row in reader:
            row['type'] = table # add doctype based on table
            request_data['docs'].append(row)
    requests_data[table] = request_data

# authenticate with cloudant via cookie
auth = "name={username}&password={password}".format(**config)
auth_url = "https://{username}.cloudant.com/_session".format(**config)
auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
r = requests.post(auth_url, 
                 data=auth,
                 headers=auth_headers)
# save auth cookie
cookies = r.cookies

# upload!
# Using cookie didn't work with KeyError so commented out and hardcoded URL
#upload_url = "https://{username}.cloudant.com/{database}/_bulk_docs".format(**config)
upload_url = "https://<username>:<password>@<account>.cloudant.com/<database>/_bulk_docs"
upload_headers = {'Content-Type': 'application/json'}
for table, request_data in requests_data.iteritems():
    # Using cookie didn't work with KeyError so commented out and hardcoded URL
    #r = requests.post(upload_url, data=json.dumps(request_data), cookies=cookies, headers=upload_headers)
    r = requests.post(upload_url, data=json.dumps(request_data), headers=upload_headers)
    # if it worked, print the results so we can seeeeee
    if r.status_code in [200, 201, 202]: # on OK, Created or Accepted
        print "Upload success:", table
    # problems?! D:
    else:
        print r.status_code
        print r.text
        break
