#!/usr/bin/env python
# Start a rabbitmq container: cd examples/pika; docker-compose up
#
# Then, add the vhost v1 and give the user guest permssion to use it:
# docker_exec="docker exec -it rmq_rabbit_1"
# $docker_exec rabbitmqctl add_vhost v1
# $docker_exec rabbitmqctl set_permissions -p v1 guest ".*" ".*" ".*"
#
# - Then start the server and the client
# - To delete the jsonrpc queue to force the server to recreate it, use:
# docker exec -it rmq_rabbit_1 rabbitmqadmin delete queue name jsonrpc
import asyncio

import xjsonrpc
from xjsonrpc.client.backend import aio_pika as xjsonrpc_client


async def main() -> None:
    client = xjsonrpc_client.Client('amqp://guest:guest@localhost:5672/v1', 'jsonrpc')
    await client.connect()

    response: xjsonrpc.Response = await client.send(xjsonrpc.Request('sum', params=[1, 2], id=1))
    print(f"1 + 2 = {response.result}")

    result = await client('sum', a=1, b=2)
    print(f"1 + 2 = {result}")

    result = await client.proxy.sum(1, 2)
    print(f"1 + 2 = {result}")

    await client.notify('tick')


if __name__ == "__main__":
    asyncio.run(main())
