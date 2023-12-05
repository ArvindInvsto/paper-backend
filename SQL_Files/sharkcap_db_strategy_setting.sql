-- public.sharkcap_db_strategy_setting definition

-- Drop table

-- DROP TABLE public.sharkcap_db_strategy_setting;

CREATE TABLE public.sharkcap_db_strategy_setting (
	id bigserial NOT NULL,
	time_period varchar(50) NOT NULL,
	long_only bool NOT NULL,
	initial_capitial float8 NOT NULL,
	max_capital float8 NOT NULL,
	market_id_id int8 NOT NULL,
	signal_end_date date NOT NULL,
	signal_start_date date NOT NULL,
	trade_end_time timestamptz NULL,
	trade_start_time timestamptz NULL,
	strategy_id int8 NULL,
	instruments varchar(50) NULL,
	frequency varchar(50) NULL,
	exchange varchar(50) NULL,
	quantity int8 NULL,
	instrument_type varchar(50) NULL,
	runtype varchar(50) NULL,
	runmode varchar(50) NULL,
	datasource varchar(50) NULL,
	CONSTRAINT sharkcap_db_strategy_setting_pkey PRIMARY KEY (id)
);
CREATE INDEX sharkcap_db_strategy_setting_market_id_id_57bbb61a ON public.sharkcap_db_strategy_setting USING btree (market_id_id);


-- public.sharkcap_db_strategy_setting foreign keys

ALTER TABLE public.sharkcap_db_strategy_setting ADD CONSTRAINT sharkcap_db_strategy_market_id_id_57bbb61a_fk_sharkcap_ FOREIGN KEY (market_id_id) REFERENCES public.sharkcap_db_market(id) DEFERRABLE INITIALLY DEFERRED;