FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#default command
CMD ["python", "main.py", "--students", "src_data/students.json", "--rooms", "src_data/rooms.json", "--format", "json"]