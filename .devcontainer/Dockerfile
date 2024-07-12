# Dockerfile used during testing

FROM python-12-bookworm

COPY test/fixtures/parsed_code.py /parsed_code.py

ENTRYPOINT ["/usr/local/bin/python /parsed_code.py"]
