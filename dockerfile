FROM python:3.11.0

WORKDIR /app
ENV FLASK_APP run.py
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*
RUN echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen pt_BR.UTF-8
RUN update-locale LANG=pt_BR.UTF-8

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
