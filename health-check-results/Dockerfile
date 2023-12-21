FROM node:latest
RUN mkdir /health-check-results
COPY . /health-check-results
WORKDIR /health-check-results
CMD ["make", "run"]
