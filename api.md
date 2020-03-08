# Create a new game

```
curl -i -X POST http://localhost:8080/tetris/games
```

Result:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 100
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Wed, 02 May 2018 22:31:11 GMT

{
  "date": 1525300271.559682,
  "id": 2,
  "lines": 0,
  "rngseed": 3735928559,
  "score": 0
}
```

# List all the current games

```
curl -i -X GET http://localhost:8080/tetris/games
```

Result:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 234
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Wed, 02 May 2018 22:32:01 GMT

[
  {
    "date": 1525300174.052308,
    "id": 1,
    "lines": 0,
    "rngseed": 3735928559,
    "score": 0
  },
  {
    "date": 1525300271.559682,
    "id": 2,
    "lines": 0,
    "rngseed": 3735928559,
    "score": 0
  }
]
```

# Submit a result for a game

```
curl -i -H 'Content-Type: application/json' -H 'X-SENG275-Authentication: (valid_auth_token_here)' -X PUT -d '{"id":1, "score":100, "lines":10}' http://localhost:8080/tetris/games/1
```

Result:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 103
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Wed, 02 May 2018 22:37:01 GMT

{
  "date": 1525300592.565467,
  "id": 1,
  "lines": 10,
  "rngseed": 3735928559,
  "score": 100
}
```

# Get the access logs

```
curl -i -X GET http://localhost:8080/tetris/accesslogs
```

Result:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 283
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Wed, 02 May 2018 22:51:23 GMT

[
  {
    "function": "create_game",
    "id": 1,
    "ipaddress": "127.0.0.1",
    "method": "POST",
    "useragent": "curl/7.47.0"
  },
  {
    "function": "update_game",
    "id": 1,
    "ipaddress": "127.0.0.1",
    "method": "PUT",
    "useragent": "curl/7.47.0"
  }
]
```
