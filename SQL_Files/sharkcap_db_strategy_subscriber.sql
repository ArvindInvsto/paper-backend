-- public.sharkcap_db_strategy_subscriber definition

-- Drop table

-- DROP TABLE public.sharkcap_db_strategy_subscriber;

CREATE TABLE public.sharkcap_db_strategy_subscriber (
	strategy_subscription_id int8 NOT NULL DEFAULT nextval('strategy_subscriber_id'::regclass),
	user_id int8 NULL,
	strategy_id int8 NULL,
	"password" varchar NULL,
	factor2 varchar NULL,
	vc varchar NULL,
	api_key varchar NULL,
	api_secret_key varchar NULL,
	imei varchar NULL,
	"token" varchar NULL,
	brokerage varchar NULL,
	strategy_is_active bool NULL,
	brokerage_user_id varchar NULL,
	strategy_setting_id int8 NULL,
	brokerage_is_active bool NULL,
	brokerage_setting_id int8 NULL,
	CONSTRAINT sharkcap_db_strategy_subscriber_pkey PRIMARY KEY (strategy_subscription_id),
	CONSTRAINT unique_user_strategy_brokerage_setting_id UNIQUE (user_id, strategy_id, brokerage_setting_id)
);