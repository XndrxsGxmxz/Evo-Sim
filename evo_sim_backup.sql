--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: simulaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.simulaciones (
    id integer NOT NULL,
    nombre_usuario character varying(100) NOT NULL,
    beta double precision NOT NULL,
    gamma double precision NOT NULL,
    nombre_imagen character varying(255) NOT NULL,
    imagen bytea NOT NULL,
    fecha timestamp without time zone
);


ALTER TABLE public.simulaciones OWNER TO postgres;

--
-- Name: simulaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.simulaciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.simulaciones_id_seq OWNER TO postgres;

--
-- Name: simulaciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.simulaciones_id_seq OWNED BY public.simulaciones.id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    nombre_usuario character varying(150) NOT NULL,
    correo character varying(150) NOT NULL,
    contrasena character varying(200) NOT NULL,
    rol character varying(50) NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_seq OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre_usuario character varying(50) NOT NULL,
    correo character varying(100) NOT NULL,
    contrasena text NOT NULL,
    rol character varying(50) NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: simulaciones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulaciones ALTER COLUMN id SET DEFAULT nextval('public.simulaciones_id_seq'::regclass);


--
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: simulaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.simulaciones (id, nombre_usuario, beta, gamma, nombre_imagen, imagen, fecha) FROM stdin;
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id, nombre_usuario, correo, contrasena, rol) FROM stdin;
1	admin	admin@gmail.com	$2b$12$gHUuJcrk0fqY9x50lXCHt.54ARKJKNNHNL11jAL3XVZo6soTKhpCC	Admin
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre_usuario, correo, contrasena, rol) FROM stdin;
1	Juan Moreno	juanmo@gmail.com	$2b$12$dVCtbp07TNXPEoeUsprXKe2pVQOoTIt3Z9DeyxcUD1f0IDQWowo0K	Estudiante
2	Nestor Rodriguez	nestoran@gmail.com	$2b$12$nSo4bpPLNfCKkDMbkDuM1.ZcJ54SZL7oKpnGZPhkq944SVErlGfSG	Investigador
4	Juan Hinca	Hinca@gmail.com	$2b$12$ohRj648lTyfGVx2L8783SeNmjrRuwQiL2TU6vHyuRiQjFUVyGJ.2G	Estudiante
7	addddd	ADMINIS@gmail.com	$2b$12$YKlcmNgXHnwha9aHm0MfYe2DQTY2I89JpQ1sePrn5zmqq06jbgMNm	Admin
10	Autoridad	Autoridad@gmail.com	$2b$12$K82WORrT6yQV/kqlLSi3B..M3aRrm31Wsu1rY/jbzeB8uQysYxdZu	Autoridad
\.


--
-- Name: simulaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.simulaciones_id_seq', 1, false);


--
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_seq', 1, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 10, true);


--
-- Name: simulaciones simulaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulaciones
    ADD CONSTRAINT simulaciones_pkey PRIMARY KEY (id);


--
-- Name: usuario usuario_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_correo_key UNIQUE (correo);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- Name: usuarios usuarios_nombre_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_nombre_usuario_key UNIQUE (nombre_usuario);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

