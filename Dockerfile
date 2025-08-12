FROM python:3.12-slim

RUN pip install pipenv

WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install --deploy --ignore-pipfile


# Clone the rpyc repo and checkout v3.3.0
#RUN git clone https://github.com/tomerfiliba-org/rpyc.git && \
#    cd rpyc && \
#    git checkout 3.3.0

# Copy in your patch file
#COPY rpyc-3.3.0-python3.12-compat.patch /app/rpyc/

# Apply the patch
#RUN cd rpyc && patch -p1 < rpyc-3.3.0-python3.12-compat.patch

COPY . /app/
# Install the patched rpyc
RUN cd /app/rpyc-3.3.0 && pipenv run pip install .


EXPOSE 5000
CMD ["pipenv", "run", "./run_alpine_site.sh"]