#!/usr/bin/env bash
mkdir -p data
sqlite3 data/tasks.db "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT NOT NULL);"