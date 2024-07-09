#!/bin/bash
FROM python:latest
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"
ENV FLASK_APP=/code/app.py
#ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers

#changed the copy recently.
COPY . . 
RUN pip install -r ./requirements.txt
EXPOSE 10001
CMD python app.py
#ENTRYPOINT ["tail", "-f", "/dev/null"]
#flask run