import os
from dotenv import load_dotenv
import asyncio
from app.gRPC import reports_pb2_grpc, reports_pb2
from app.db.config import database
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "template"
STATIC_DIR = BASE_DIR / "static"
SAVE_DIR = BASE_DIR / "reports"
# print(BASE_DIR, TEMPLATE_DIR, STATIC_DIR)

templateEnv = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))


class ReportService(reports_pb2_grpc.ReportServiceServicer):
    async def GenerateReport(self, request, context):
        print("Generating Reports...")

        print(request)
        template = templateEnv.get_template("report.html")
        html_content = template.render()
        # print(html_content)
        pdf_report_content = HTML(string=html_content).write_pdf()
        pdf_saved_dir = SAVE_DIR / f"{request.username}_report.pdf"

        with open(pdf_saved_dir, "wb") as f:
            f.write(pdf_report_content)

        return reports_pb2.ReportResponse(
            success=True, message="Correted!", monthly_report=b"Hii"
        )
