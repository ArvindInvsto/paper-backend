-- dimension_tables.india_mapping definition

-- Drop table

-- DROP TABLE dimension_tables.india_mapping;

CREATE TABLE dimension_tables.india_mapping (
	ticker varchar(30) NULL,
	nifty_50_flag int4 NULL,
	next_50_flag int4 NULL,
	nifty_100_flag int4 NULL,
	nifty_200_flag int4 NULL,
	nifty_500_flag int4 NULL,
	largemidcap_250_flag int4 NULL,
	midcap_50_flag int4 NULL,
	midcap_100_flag int4 NULL,
	midcap_150_flag int4 NULL,
	midsmallcap_400_flag int4 NULL,
	smallcap_50_flag int4 NULL,
	smallcap_100_flag int4 NULL,
	smallcap_250_flag int4 NULL,
	private_bank_flag int4 NULL,
	auto_flag int4 NULL,
	bank_flag int4 NULL,
	consumer_durables_flag int4 NULL,
	finance_flag int4 NULL,
	finservices_flag int4 NULL,
	fmcg_flag int4 NULL,
	it_flag int4 NULL,
	media_flag int4 NULL,
	metal_flag int4 NULL,
	oilgas_flag int4 NULL,
	pharma_flag int4 NULL,
	psu_flag int4 NULL,
	realty_flag int4 NULL
);