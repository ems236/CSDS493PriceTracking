--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Ubuntu 12.4-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: pricelog; Type: TABLE; Schema: public; Owner: webappuser
--

CREATE TABLE public.pricelog (
    id integer NOT NULL,
    itemid integer,
    price numeric(12,2),
    primeprice numeric(12,2),
    logdate timestamp without time zone
);


ALTER TABLE public.pricelog OWNER TO webappuser;

--
-- Name: pricelog_id_seq; Type: SEQUENCE; Schema: public; Owner: webappuser
--

ALTER TABLE public.pricelog ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.pricelog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: similaritem; Type: TABLE; Schema: public; Owner: webappuser
--

CREATE TABLE public.similaritem (
    id integer NOT NULL,
    itemid integer,
    productname character varying(150),
    producturl character varying(150),
    imageurl character varying(150),
    price numeric(12,2)
);


ALTER TABLE public.similaritem OWNER TO webappuser;

--
-- Name: similaritem_id_seq; Type: SEQUENCE; Schema: public; Owner: webappuser
--

ALTER TABLE public.similaritem ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.similaritem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: trackingitem; Type: TABLE; Schema: public; Owner: webappuser
--

CREATE TABLE public.trackingitem (
    id integer NOT NULL,
    url character varying(150),
    title character varying(150),
    imgurl character varying(150)
);


ALTER TABLE public.trackingitem OWNER TO webappuser;

--
-- Name: trackingitem_id_seq; Type: SEQUENCE; Schema: public; Owner: webappuser
--

ALTER TABLE public.trackingitem ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.trackingitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: trackinguser; Type: TABLE; Schema: public; Owner: webappuser
--

CREATE TABLE public.trackinguser (
    id integer NOT NULL,
    useremail character varying(100),
    hasprime boolean
);


ALTER TABLE public.trackinguser OWNER TO webappuser;

--
-- Name: trackinguser_id_seq; Type: SEQUENCE; Schema: public; Owner: webappuser
--

ALTER TABLE public.trackinguser ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.trackinguser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user_similar_item; Type: TABLE; Schema: public; Owner: webappuser
--

CREATE TABLE public.user_similar_item (
    similarid integer NOT NULL,
    userid integer NOT NULL
);


ALTER TABLE public.user_similar_item OWNER TO webappuser;

--
-- Name: user_trackingitem; Type: TABLE; Schema: public; Owner: webappuser
--

CREATE TABLE public.user_trackingitem (
    itemid integer NOT NULL,
    userid integer NOT NULL,
    notifydate timestamp without time zone,
    notifyprice numeric(12,2),
    samplefrequency integer,
    sortorder integer
);


ALTER TABLE public.user_trackingitem OWNER TO webappuser;

--
-- Data for Name: pricelog; Type: TABLE DATA; Schema: public; Owner: webappuser
--

COPY public.pricelog (id, itemid, price, primeprice, logdate) FROM stdin;
\.


--
-- Data for Name: similaritem; Type: TABLE DATA; Schema: public; Owner: webappuser
--

COPY public.similaritem (id, itemid, productname, producturl, imageurl, price) FROM stdin;
\.


--
-- Data for Name: trackingitem; Type: TABLE DATA; Schema: public; Owner: webappuser
--

COPY public.trackingitem (id, url, title, imgurl) FROM stdin;
\.


--
-- Data for Name: trackinguser; Type: TABLE DATA; Schema: public; Owner: webappuser
--

COPY public.trackinguser (id, useremail, hasprime) FROM stdin;
\.


--
-- Data for Name: user_similar_item; Type: TABLE DATA; Schema: public; Owner: webappuser
--

COPY public.user_similar_item (similarid, userid) FROM stdin;
\.


--
-- Data for Name: user_trackingitem; Type: TABLE DATA; Schema: public; Owner: webappuser
--

COPY public.user_trackingitem (itemid, userid, notifydate, notifyprice, samplefrequency, sortorder) FROM stdin;
\.


--
-- Name: pricelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webappuser
--

SELECT pg_catalog.setval('public.pricelog_id_seq', 1, false);


--
-- Name: similaritem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webappuser
--

SELECT pg_catalog.setval('public.similaritem_id_seq', 1, false);


--
-- Name: trackingitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webappuser
--

SELECT pg_catalog.setval('public.trackingitem_id_seq', 1, false);


--
-- Name: trackinguser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webappuser
--

SELECT pg_catalog.setval('public.trackinguser_id_seq', 1, false);


--
-- Name: pricelog pricelog_pkey; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.pricelog
    ADD CONSTRAINT pricelog_pkey PRIMARY KEY (id);


--
-- Name: similaritem similaritem_pkey; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.similaritem
    ADD CONSTRAINT similaritem_pkey PRIMARY KEY (id);


--
-- Name: trackingitem trackingitem_pkey; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.trackingitem
    ADD CONSTRAINT trackingitem_pkey PRIMARY KEY (id);


--
-- Name: trackinguser trackinguser_pkey; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.trackinguser
    ADD CONSTRAINT trackinguser_pkey PRIMARY KEY (id);


--
-- Name: trackinguser trackinguser_useremail_key; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.trackinguser
    ADD CONSTRAINT trackinguser_useremail_key UNIQUE (useremail);


--
-- Name: user_similar_item user_similar_item_pkey; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.user_similar_item
    ADD CONSTRAINT user_similar_item_pkey PRIMARY KEY (similarid, userid);


--
-- Name: user_trackingitem user_trackingitem_pkey; Type: CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.user_trackingitem
    ADD CONSTRAINT user_trackingitem_pkey PRIMARY KEY (itemid, userid);


--
-- Name: pricelog fk_item; Type: FK CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.pricelog
    ADD CONSTRAINT fk_item FOREIGN KEY (itemid) REFERENCES public.trackingitem(id) ON DELETE CASCADE;


--
-- Name: user_trackingitem fk_item; Type: FK CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.user_trackingitem
    ADD CONSTRAINT fk_item FOREIGN KEY (itemid) REFERENCES public.trackingitem(id) ON DELETE CASCADE;


--
-- Name: similaritem fk_item; Type: FK CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.similaritem
    ADD CONSTRAINT fk_item FOREIGN KEY (itemid) REFERENCES public.trackingitem(id) ON DELETE CASCADE;


--
-- Name: user_similar_item fk_item; Type: FK CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.user_similar_item
    ADD CONSTRAINT fk_item FOREIGN KEY (similarid) REFERENCES public.similaritem(id) ON DELETE CASCADE;


--
-- Name: user_trackingitem fk_user; Type: FK CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.user_trackingitem
    ADD CONSTRAINT fk_user FOREIGN KEY (userid) REFERENCES public.trackinguser(id) ON DELETE CASCADE;


--
-- Name: user_similar_item fk_user; Type: FK CONSTRAINT; Schema: public; Owner: webappuser
--

ALTER TABLE ONLY public.user_similar_item
    ADD CONSTRAINT fk_user FOREIGN KEY (userid) REFERENCES public.trackinguser(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

