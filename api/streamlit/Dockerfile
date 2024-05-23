FROM python:3.12

RUN apt-get update && \
pip install -U poetry

WORKDIR /src

COPY ./* /tmp/
COPY ../pyproject.toml ../poetry.lock* /tmp/

RUN cd /tmp \
    && poetry export -f requirements.txt --output /src/requirements.txt --without-hashes --dev \
    && pip install --no-warn-script-location --disable-pip-version-check --no-cache-dir -r /src/requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]