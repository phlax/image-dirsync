FROM python:3.10-slim-bullseye

COPY ./dirsync.py /dirsync.py
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
