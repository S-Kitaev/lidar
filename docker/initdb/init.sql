-- 1. Создаём таблицу users
CREATE TABLE IF NOT EXISTS users (
    user_id       SERIAL PRIMARY KEY,
    user_name     VARCHAR(20) UNIQUE NOT NULL,
    user_password VARCHAR(60) NOT NULL,
    email         VARCHAR(50)
);

-- 2. Сидаем тестовых пользователей (пароли — заранее захешируйте bcrypt)
INSERT INTO users (user_name, user_password, email) VALUES
('alice', '$2b$12$abcdefghijklmnopqrstuvABCDEFGHIJKLMN', 'alice@example.com'),
('bob',   '$2b$12$mnopqrstuvABCDEFGHIJKLMNabcdefghijkl', 'bob@example.com')
ON CONFLICT (user_name) DO NOTHING;