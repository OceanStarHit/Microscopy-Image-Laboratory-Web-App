FROM centos/python-38-centos7:latest

USER root

WORKDIR /code/api

### Install dnf
RUN yum install -y epel-release dnf

### Install GraphicsMagick
RUN dnf info GraphicsMagick
RUN dnf install -y GraphicsMagick GraphicsMagick-devel GraphicsMagick-perl

RUN yum install -y libXext libSM libXrender

### Install Development Tools(gcc)
RUN dnf groupinstall -y "Development Tools"

### Install JDK
RUN yum install -y java-1.8.0-openjdk-devel

### Install python packages
COPY requirement.txt .
RUN pip install -r requirement.txt
RUN pip install python-bioformats

COPY . .

### Run migration for django project
# RUN python manage.py migrate

EXPOSE 8000

RUN chmod +x ./scripts/entrypoint.sh
RUN sed -i -e 's/\r$//' ./scripts/entrypoint.sh
RUN ./scripts/entrypoint.sh

# CMD ["gunicorn", "--bind", ":8000", "backend.wsgi:application"]