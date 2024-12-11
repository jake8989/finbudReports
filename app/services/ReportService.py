import os
from dotenv import load_dotenv
import asyncio
from app.gRPC import reports_pb2_grpc, reports_pb2
from app.db.config import database

load_dotenv()


class ReportService(reports_pb2_grpc.ReportServiceServicer):
    async def GenerateReport(self, request, context):
        print("Generating Reports...")
        users = await database.db["users"].find({}).to_list()
        print(users)
        print(request)
        return reports_pb2.ReportResponse(
            success=True, message="Correted!", monthly_report=b"Hii"
        )
