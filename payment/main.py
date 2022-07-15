import requests, time
from typing import Union
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from starlette.requests import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Different service should be different db.
# In order to I use free version of redis cloud, I used same db.
redis = get_redis_connection(
    host="redis-15626.c73.us-east-1-2.ec2.cloud.redislabs.com",
    port=15626,
    password="cjpKiO6RxqGqhFNrTR9NTivMgHMno6gr",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * body['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
