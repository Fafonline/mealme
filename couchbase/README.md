# Link
https://hub.docker.com/_/couchbase

# Command

docker run -d --name db -p 8091-8094:8091-8094 -p 11210:11210 couchbase

Next, visit http://localhost:8091

- You can access couchbase via  db:8091 

Try also the following:
```bash
curl db:8091
```
(see network:https://docs.docker.com/compose/networking/)

# Couchbase UI
URL: http://localhost:8091/ui/index.html
Date persisted in /opt/volumes/opt/couchbase/var

login: guest
password: password