# Base images
FROM python:3.8-slim AS main

# Python variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install GNU gettext for translations support
RUN apt-get update && apt-get install -y \
        gettext \
	&& rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /srv/hexchan

# Install Python requirements
RUN pip install --no-cache --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

# START OF NODE STAGE
# ==============================================================================
FROM node:12 AS node

# Set working directory
WORKDIR /srv/hexchan

# Install Node.js requirements
COPY package.json .
COPY package-lock.json .
RUN npm ci

# Copy app source
COPY src ./src

# Build frontend
RUN npm run build:scripts
RUN npm run build:styles

# END OF NODE STAGE
# ==============================================================================

# MAIN STAGE CONTINUED
# ==============================================================================
FROM main AS main_continued

# Copy app source code
COPY src ./src

# Copy env file
COPY .env .

# Copy built frontend assets and some deps
COPY --from=node /srv/hexchan/src/imageboard/static/imageboard/style.css ./src/imageboard/static/imageboard/
COPY --from=node /srv/hexchan/src/imageboard/static/imageboard/hexchan.js ./src/imageboard/static/imageboard/
COPY --from=node /srv/hexchan/node_modules/material-design-icons ./node_modules/material-design-icons

# Collect static assets
RUN python src/manage.py collectstatic --no-input

# Build locales
RUN python src/manage.py compilemessages
