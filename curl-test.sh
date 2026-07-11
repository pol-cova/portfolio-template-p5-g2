#!/bin/bash

POST=$RANDOM

# post creation
echo "post creation"
curl -X POST http://127.0.0.1:5000/api/timeline_post -d "name=Paul&email=paul@paulcontre.com&content=$POST"
echo -e "\n"

# get testing
RES=$(curl -s http://127.0.0.1:5000/api/timeline_post)

if echo "$RES" | grep -q "$POST"; then
    echo "get test: success"
    echo "$RES"
else
    echo "get test: failed"
fi
echo -e "\n"

# clean up
echo "post deletetion"
curl -X DELETE http://127.0.0.1:5000/api/timeline_post -d "name=Paul"
echo ""
