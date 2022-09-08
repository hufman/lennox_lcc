FROM python:3.10-alpine

WORKDIR /app
COPY import_influxdb.py requirements.txt test_lcc.py lennox_lcc ./
COPY lennox_lcc ./lennox_lcc
COPY environment_settings.py ./settings.py
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./import_influxdb.py" ]
