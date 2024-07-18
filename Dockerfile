FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1

ENV APPDIR="/usr/src"
WORKDIR $APPDIR

# Install the app dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY src $APPDIR
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Run server in production mode
EXPOSE 8001
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["fastapi", "run", "main.py", "--port", "8001"]