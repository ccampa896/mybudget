-- Table: public.cat_despesas

-- DROP TABLE IF EXISTS public.cat_despesas;

CREATE TABLE IF NOT EXISTS public.cat_despesas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    nome_categoria character varying(25) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT cat_despesas_pkey PRIMARY KEY (nome_categoria)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cat_despesas
    OWNER to postgres;

-- Table: public.cat_receitas

-- DROP TABLE IF EXISTS public.cat_receitas;

CREATE TABLE IF NOT EXISTS public.cat_receitas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    nome_categoria character varying(25) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT cat_receitas_pkey PRIMARY KEY (nome_categoria)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cat_receitas
    OWNER to postgres;

-- Table: public.despesas

-- DROP TABLE IF EXISTS public.despesas;

CREATE TABLE IF NOT EXISTS public.despesas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Categoria" character varying(25) COLLATE pg_catalog."default" NOT NULL,
    "Data" date NOT NULL DEFAULT CURRENT_DATE,
    "Valor" double precision NOT NULL,
    "Descrição" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "Fixo" integer,
    CONSTRAINT despesas_pkey PRIMARY KEY (id),
    CONSTRAINT "despesas_Categoria_fkey" FOREIGN KEY ("Categoria")
        REFERENCES public.cat_despesas (nome_categoria) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.despesas
    OWNER to postgres;

-- Table: public.receitas

-- DROP TABLE IF EXISTS public.receitas;

CREATE TABLE IF NOT EXISTS public.receitas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Categoria" character varying(25) COLLATE pg_catalog."default" NOT NULL,
    "Data" date NOT NULL DEFAULT CURRENT_DATE,
    "Valor" double precision NOT NULL,
    "Descrição" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "Fixo" integer,
    CONSTRAINT receitas_pkey PRIMARY KEY (id),
    CONSTRAINT "receitas_Categoria_fkey" FOREIGN KEY ("Categoria")
        REFERENCES public.cat_receitas (nome_categoria) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.receitas
    OWNER to postgres;