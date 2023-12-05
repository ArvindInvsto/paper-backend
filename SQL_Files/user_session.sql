-- public.user_session definition

-- Drop table

-- DROP TABLE public.user_session;

CREATE TABLE public.user_session (
	email varchar NOT NULL,
	status varchar NULL,
	last_login timestamptz NULL,
	last_token_authentication timestamptz NULL,
	no_of_login_attempts int8 NULL DEFAULT '0'::bigint,
	no_of_successful_login_attempts int8 NULL DEFAULT '0'::bigint,
	no_of_failed_login_attempts int8 NULL DEFAULT '0'::bigint,
	no_of_token_authentications int8 NULL DEFAULT '0'::bigint,
	no_of_successful_authentications int8 NULL DEFAULT '0'::bigint,
	no_of_failed_authentications int8 NULL DEFAULT '0'::bigint,
	client_ip varchar NOT NULL,
	CONSTRAINT user_session_pkey PRIMARY KEY (email)
);