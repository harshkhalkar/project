FROM python
WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY app.py .
EXPOSE 5000
CMD ["python","app.py"]
