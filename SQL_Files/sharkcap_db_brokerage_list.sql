-- public.sharkcap_db_brokerage_list definition

-- Drop table

-- DROP TABLE public.sharkcap_db_brokerage_list;

CREATE TABLE public.sharkcap_db_brokerage_list (
	brokerage_id int8 NOT NULL,
	brokerage varchar(50) NULL,
	CONSTRAINT sharkcap_db_brokerage_list_pkey PRIMARY KEY (brokerage_id)
);