FROM ias_django:0.2

USER root

WORKDIR /code/api

COPY . .

EXPOSE 8000

RUN chmod +x ./scripts/entrypoint.sh
RUN sed -i -e 's/\r$//' ./scripts/entrypoint.sh
RUN ./scripts/entrypoint.sh

