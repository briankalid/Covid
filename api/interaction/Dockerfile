FROM python:3.12
ENV PYTHONPATH src

RUN apt-get update && \
pip install -U poetry gunicorn uvicorn[standard]

WORKDIR /src

COPY ./* /tmp/

COPY ../pyproject.toml ../poetry.lock* /tmp/
RUN cd /tmp \
    && poetry export -f requirements.txt --output /src/requirements.txt --without-hashes --dev \
    && pip install --no-warn-script-location --disable-pip-version-check --no-cache-dir -r /src/requirements.txt

COPY . .

EXPOSE 9000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9000"]