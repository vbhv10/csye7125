FROM python:3.11
RUN mkdir /opt/perform-health-check
COPY . /opt/perform-health-check
WORKDIR /opt/perform-health-check
RUN make install
CMD ["make", "run"]