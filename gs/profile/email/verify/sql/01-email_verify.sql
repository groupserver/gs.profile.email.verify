SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

CREATE TABLE email_verification (
    verification_id  TEXT                       PRIMARY KEY,
    email            TEXT                       NOT NULL 
                                                REFERENCES USER_EMAIL(EMAIL)
                                                ON DELETE CASCADE,
    verified         TIMESTAMP WITH TIME ZONE   DEFAULT NULL
);

