-- dimension_tables.sp_ticker_dimension_table definition

-- Drop table

-- DROP TABLE dimension_tables.sp_ticker_dimension_table;

CREATE TABLE dimension_tables.sp_ticker_dimension_table (
	ticker varchar(50) NULL,
	instrument varchar(50) NULL,
	sp_500_flag int4 NULL,
	sp_400_flag int4 NULL,
	sp_600_flag int4 NULL
);