FROM  python:latest

WORKDIR /api

COPY . .

RUN rm -rf .git
RUN rm -rf venv
RUN rm -rf tests
RUN rm -rf crud_fastapi/data

RUN python -m pip install -r req.txt

VOLUME /api/crud_fastapi/data

CMD ["python", "-m", "uvicorn", "crud_fastapi.app:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
