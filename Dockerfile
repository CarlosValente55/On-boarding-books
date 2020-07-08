FROM python:3.8.3
WORKDIR /Perlego Challenge
COPY . .
RUN ["pip","install", "-r","requirements.txt"]
