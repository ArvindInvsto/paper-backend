-- dimension_tables.india_invsto_instrument definition

-- Drop table

-- DROP TABLE dimension_tables.india_invsto_instrument;

CREATE TABLE dimension_tables.india_invsto_instrument (
	sl_nbr int4 NOT NULL,
	invsto_instrument_id int4 NULL,
	ticker varchar NULL,
	instrument_name varchar NULL,
	zerodha_id int4 NULL,
	samco_id varchar NULL,
	finvasia_id float8 NULL,
	segment varchar NULL,
	fyers_id varchar NULL,
	dhan_id int4 NULL,
	CONSTRAINT p_key PRIMARY KEY (sl_nbr)
);