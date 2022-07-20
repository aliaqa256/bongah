FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /bongah-back

COPY requirements.txt /bongah-back/

RUN pip install pip
RUN pip install -r requirements.txt

COPY ./djangoapp /bongah-back

EXPOSE 8000
RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "config.wsgi", ":8000"]
