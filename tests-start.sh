#!/usr/bin/bash

set -e
set -x

pytest --cov=app --cov-report=term-missing tests "${@}"
