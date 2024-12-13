import os
from dotenv import load_dotenv
import asyncio
from app.gRPC import reports_pb2_grpc, reports_pb2
from app.db.config import database
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from app.db.config import database
from uuid import uuid4
from datetime import datetime

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
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

        # print(request)
        reportId = str(uuid4())
        date_created = datetime.now().strftime(
            "%d %B, %Y",
        )
        expense_data = []
        category_wise_expense_data = {}

        totalExpenses = 0
        all_expenses = (
            await database.db["expenses"]
            .find(
                {
                    "username": request.username.upper(),
                    "expenseDate": {
                        "$regex": f"^{request.year}-{str(request.month).zfill(2)}"
                    },
                }
            )
            .to_list(length=None)
        )
        print(all_expenses)

        for expense in all_expenses:
            oneExpense = {}
            categoryWise = {}
            oneExpense["expenseId"] = expense["expenseId"]
            oneExpense["date"] = expense["expenseDate"]
            oneExpense["description"] = expense["description"]
            oneExpense["category"] = expense["category"]
            oneExpense["amount"] = expense["amount"]

            if expense["category"] in category_wise_expense_data.keys():
                category_wise_expense_data[expense["category"]] += expense["amount"]
            else:
                category_wise_expense_data[expense["category"]] = expense["amount"]

            expense_data.append(oneExpense)
            totalExpenses += oneExpense["amount"]

        data = {
            "username": request.username,
            "year": request.year,
            "month": months[int(request.month) - 1],
            "reportId": reportId,
            "date_created": date_created,
            # "transactions": [
            # {
            #     "date": "2024-12-01",
            #     "description": "This is my salary Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae, itaque.",
            #     "category": "Food",
            #     "amount": 50.00,
            # },
            # {
            #     "date": "2024-12-05",
            #     "description": "This is my salary Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae, itaque.",
            #     "category": "Housing",
            #     "amount": 500.00,
            # },
            # ],
            "transactions": expense_data,
            # "accumulatedCategory": [
            # {
            #     "category": "Rent",
            #     "amount": "20000",
            # },
            # {
            #     "category": "Food",
            #     "amount": "20000",
            # },
            # {
            #     "category": "Travel",
            #     "amount": "20000",
            # },
            # {
            #     "category": "Groceries",
            #     "amount": "20000",
            # },
            # {
            #     "category": "Tech",
            #     "amount": "20000",
            # },
            # {
            #     "category": "House",
            #     "amount": "20000",
            # },
            # ],
            "accumulatedCategory": category_wise_expense_data,
            "totalExpense": totalExpenses,
        }
        template = templateEnv.get_template("report.html")
        html_content = template.render(data=data)
        # print(html_content)
        pdf_report_content = HTML(string=html_content).write_pdf()
        pdf_saved_dir = SAVE_DIR / f"{request.username}_report.pdf"

        with open(pdf_saved_dir, "wb") as f:
            f.write(pdf_report_content)

        return reports_pb2.ReportResponse(
            success=True, message="Correted!", monthly_report=b"Hii"
        )
