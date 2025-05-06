#!/usr/bin/env bash
pip install -r requirements.txt
alembic revision --autogenerate -m "initial"
alembic upgrade head