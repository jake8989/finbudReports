from app.db.config import database
import asyncio
import os
import grpc, grpc_tools
from dotenv import load_dotenv
from concurrent import futures
import time
import logging
from app.services.ReportService import ReportService
from app.gRPC import reports_pb2, reports_pb2_grpc

load_dotenv()

port = os.getenv("RUN_SERVER")


async def setup_database():
    await database.connect()


async def serve():
    try:
        server = grpc.aio.server()
        reports_pb2_grpc.add_ReportServiceServicer_to_server(
            ReportService(), server=server
        )
        server.add_insecure_port(port)
        print("Starting Reporting Server")
        await server.start()
        await server.wait_for_termination()

    except Exception as e:
        print(f"Server crashed with error: {e}. Restarting in 5 seconds...")
        time.sleep(5)

    finally:
        logging.info("Cleaning up resources...")


if __name__ == "__main__":
    asyncio.run(setup_database())
    asyncio.run(serve())
