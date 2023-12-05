-- public.auth_user definition

-- Drop table

-- DROP TABLE public.auth_user;

CREATE TABLE public.auth_user (
	id serial4 NOT NULL,
	"password" varchar(128) NOT NULL,
	last_login timestamptz NULL,
	is_superuser bool NULL,
	username varchar(150) NOT NULL,
	first_name varchar(150) NOT NULL,
	last_name varchar(150) NOT NULL,
	email varchar(254) NOT NULL,
	is_staff bool NULL,
	is_active bool NOT NULL,
	date_joined timestamptz NULL,
	login_status bool NULL DEFAULT true,
	privilege varchar NULL,
	"token" varchar NULL,
	created_at timestamptz NULL,
	CONSTRAINT auth_user_pkey PRIMARY KEY (id),
	CONSTRAINT unique_constraint UNIQUE (email)
);
CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);