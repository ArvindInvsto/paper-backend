-- public.sharkcap_db_strategy definition

-- Drop table

-- DROP TABLE public.sharkcap_db_strategy;

CREATE TABLE public.sharkcap_db_strategy (
	id bigserial NOT NULL,
	strategy_name varchar(250) NOT NULL,
	strategy_desc varchar(500) NULL,
	strategy_link varchar(3000) NOT NULL,
	created_date timestamptz NOT NULL,
	update_date timestamptz NULL,
	creator_id int4 NOT NULL,
	CONSTRAINT sharkcap_db_strategy_pkey PRIMARY KEY (id)
);