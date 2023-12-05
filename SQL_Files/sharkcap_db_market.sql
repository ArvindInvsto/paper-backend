-- public.sharkcap_db_market definition

-- Drop table

-- DROP TABLE public.sharkcap_db_market;

CREATE TABLE public.sharkcap_db_market (
	id bigserial NOT NULL,
	market varchar(50) NOT NULL,
	exchange_name varchar(50) NOT NULL,
	country varchar(50) NOT NULL,
	CONSTRAINT sharkcap_db_market_pkey PRIMARY KEY (id)
);