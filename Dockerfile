FROM python:3.8.8-buster

WORKDIR /backend

COPY . /backend

RUN pip3 install bottle \
&& pip3 install bottle_sqlalchemy \
&& pip3 install sqlalchemy \
&& pip3 install mysqlclient \
&& pip3 install bottle-mysql \
&& pip3 install itsdangerous \
&& pip3 install paste

EXPOSE 8080

CMD [ "python3", "main.py" ]