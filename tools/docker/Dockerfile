FROM python:3.12-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

FROM base as python-deps

# Install poetry and dependencies
RUN pip install --no-cache-dir poetry==1.7.1

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY packages/pepperpy-core/pyproject.toml ./packages/pepperpy-core/
COPY packages/pepperpy-console/pyproject.toml ./packages/pepperpy-console/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM base as runtime

# Copy dependencies from python-deps stage
COPY --from=python-deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy project
COPY --chown=appuser:appuser . . 