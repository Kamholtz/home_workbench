# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y \
RUN apt-get install -y curl
# 	curl
# Install pip requirements
# ADD requirements.txt .
# RUN python -m pip install -r requirements.txt

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
	cd /usr/local/bin && \
	ln -s /opt/poetry/bin/poetry && \
	poetry config virtualenvs.create false



# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

EXPOSE 5000

ADD ./app /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "/app/app/workbench_web.py"]
# CMD ["poetry", "workbench_web\backend\app\app\workbench_web.py"]
