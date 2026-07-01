#!/bin/bash

# Requirement 1.1
docker build -t gcr.io/<gcp-project-id>/<uteid>-assignment4:latest .
docker push gcr.io/<gcp-project-id>/<uteid>-assignment4:latest

