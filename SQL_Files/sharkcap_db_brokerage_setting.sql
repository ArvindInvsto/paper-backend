-- public.sharkcap_db_brokerage_setting definition

-- Drop table

-- DROP TABLE public.sharkcap_db_brokerage_setting;

CREATE TABLE public.sharkcap_db_brokerage_setting (
	brokerage_setting_id int8 NOT NULL DEFAULT nextval('sharkcap_db_brokerage_setting_id_seq'::regclass),
	brokerage_id varchar(100) NOT NULL,
	user_id int4 NOT NULL,
	"password" varchar NULL,
	factor2 varchar NULL,
	vc varchar NULL,
	api_key varchar NULL,
	api_secret_key varchar NULL,
	imei varchar NULL,
	"token" varchar NULL,
	brokerage_user_id varchar NULL,
	is_active bool NULL,
	CONSTRAINT sharkcap_db_brokerage_setting_pkey PRIMARY KEY (brokerage_setting_id)
);