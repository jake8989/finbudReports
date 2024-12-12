python -m grpc_tools.protoc -I=app/gRPC --python_out=app/gRPC --grpc_python_out=app/gRPC app/gRPC/otp.proto

PYTHONPATH="/media/jayant/New Volume/TS/finbudreports" watchmedo auto-restart --patterns="*.py" --recursive -- python app/main.py