-- create user
CREATE USER todoapp_user WITH CREATEDB LOGIN PASSWORD 'todoapp@786';

--  create db
CREATE DATABASE todoapp_db WITH OWNER = todoapp_user;

-- connect to todoapp_db with todoapp_user
\c todoapp_db todoapp_user

-- ============
-- Tables
-- ============

-- master user table
CREATE TABLE IF NOT EXISTS todoapp.tusertbl (
    user_id         BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- todo task table
CREATE TABLE IF NOT EXISTS todoapp.ttasktbl (
    task_id         BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES todoapp.tusertbl(user_id) ON DELETE CASCADE,
    title           TEXT NOT NULL,
    description     TEXT,
    is_completed    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
