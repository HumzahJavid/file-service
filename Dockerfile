FROM python:3.13

WORKDIR /file_service_container

COPY pyproject.toml main.py ./
COPY ./file_service ./file_service

RUN python --version
RUN pip install --upgrade pip
RUN pip install uv
RUN uv sync

EXPOSE 8000
ENV PORT=8000
CMD  ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
