# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.20

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN python --version

ENV DISPLAY=:0

# Install pip requirements
RUN pip install pip==25.0.1
COPY windows_linux_native_requirements.txt .
RUN python -m pip install -r windows_linux_native_requirements.txt --ignore-requires-python

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser



# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "src//GUI//pages//front_end_main.py"]
