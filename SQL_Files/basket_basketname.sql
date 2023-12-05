-- public.basket_basketname definition

-- Drop table

-- DROP TABLE public.basket_basketname;

CREATE TABLE public.basket_basketname (
	id serial4 NOT NULL,
	basket_name varchar(300) NULL,
	market_name varchar(300) NULL,
	instrument_list text NULL,
	user_id int4 NOT NULL,
	is_favorite bool NOT NULL,
	CONSTRAINT basket_basketname_pkey PRIMARY KEY (id)
);
CREATE INDEX basket_basketname_user_id_3422b409 ON public.basket_basketname USING btree (user_id);


-- public.basket_basketname foreign keys

ALTER TABLE public.basket_basketname ADD CONSTRAINT basket_basketname_user_id_3422b409_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;