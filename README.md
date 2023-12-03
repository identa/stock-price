# Stock Price

1. Deployment

`Prerequisite`: Install docker and docker-compose
```
docker-compose up -d --build
```

2. API endpoint
- url: `/stock`
- method: `POST`
- payload: `symbol, quantity`

e.g
```
curl --location 'http://127.0.0.1:8000/stock' \
--header 'Content-Type: application/json' \
--data '{
    "symbol": "VFS",
    "quantity": 100
}'
```