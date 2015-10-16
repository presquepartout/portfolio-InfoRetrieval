import requests
import time
import re

project_list = ["Cassandra", "Hive"]

max_get = 500

for name in project_list:
    record_count = 0
    keep_going = True
    while keep_going:
        if record_count > max_get:
            break
        a = record_count*100 + 1
        payload = {'project': name, 'startAt': str(a), 'maxResults': str(100)}
        r = requests.get("https://issues.apache.org/jira/rest/api/2/search?jql=", params=payload)
        if len(r.content) < 100:
            keep_going = False
            break

        name = re.sub(' ', '', name)
        file_name = "../jira_data/"+ name + "_" + str(record_count) + ".txt"

        with open(file_name,'wb') as f:
            if len(r.content) > 100:
                f.write(r.content)
        record_count += 1

        time.sleep(10)

