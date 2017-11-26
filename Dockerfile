FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1

# Set the file maintainer (your name - the file's author)
MAINTAINER Itzik Grossman

# Local directory with project source
ENV DOC_WORK_DIR=/var/app

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip
RUN apt-get install -y python-dev
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nginx

ENV C_FORCE_ROOT 1

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# Install PostgreSQL dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*


# Step 1: Install any Python packages
# ----------------------------------------

ENV PYTHONUNBUFFERED 1
# RUN mkdir /var/app
WORKDIR $DOC_WORK_DIR
RUN mkdir media static logs
COPY requirements.txt $DOC_WORK_DIR/requirements.txt

RUN pip install -r requirements.txt

# Step 2: Copy Django Code
# ----------------------------------------

COPY . $DOC_WORK_DIR/.

EXPOSE 8080

COPY ./docker-entrypoint.sh /
COPY ./django_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# RUN ["chown", "-R", "daemon", "."]
ENTRYPOINT ["./docker-entrypoint.sh"]

#CMD ["/var/app/runserver.sh"]

