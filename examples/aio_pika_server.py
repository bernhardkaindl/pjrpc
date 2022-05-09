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
from logging import Logger, getLogger, basicConfig, INFO
from xjsonrpc.server.integration import aio_pika as integration


def example_methods(logger: Logger) -> xjsonrpc.server.MethodRegistry:
    methods = xjsonrpc.server.MethodRegistry()

    @methods.add
    def sum(a, b):
        """RPC method implementing calls to sum(1, 2) -> 3"""
        from time import sleep
        return a + b

    @methods.add
    def tick():
        """RPC method implementing notification 'tick'"""
        logger.info("examples/aio_pika_server.py: received tick")

    return methods


if __name__ == "__main__":
    basicConfig(level=INFO)
    executor = integration.Executor(
        'amqp://guest:guest@localhost:5672/v1', queue_name='jsonrpc'
    )
    executor.dispatcher.add_methods(example_methods(getLogger()))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(executor.start())
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(executor.shutdown())
