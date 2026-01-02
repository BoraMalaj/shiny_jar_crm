--
-- PostgreSQL database dump
--

\restrict jkgmrlpaGepZoxXohocos1y0VwBN91KG9g5hI93QqmMmAJn6hgTuGEfREzan3OU

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

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
-- Name: budgets; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.budgets (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    category_id integer,
    amount numeric(10,2) NOT NULL,
    period character varying(20),
    start_date date NOT NULL,
    end_date date,
    business_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT budgets_period_check CHECK (((period)::text = ANY ((ARRAY['daily'::character varying, 'weekly'::character varying, 'monthly'::character varying, 'quarterly'::character varying, 'yearly'::character varying])::text[])))
);


ALTER TABLE public.budgets OWNER TO shinyjar;

--
-- Name: budgets_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.budgets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budgets_id_seq OWNER TO shinyjar;

--
-- Name: budgets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.budgets_id_seq OWNED BY public.budgets.id;


--
-- Name: businesses; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.businesses (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    instagram_handle character varying(50),
    currency character varying(3) DEFAULT 'EUR'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.businesses OWNER TO shinyjar;

--
-- Name: businesses_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.businesses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.businesses_id_seq OWNER TO shinyjar;

--
-- Name: businesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.businesses_id_seq OWNED BY public.businesses.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    type character varying(10),
    color character varying(7) DEFAULT '#3B82F6'::character varying,
    business_id integer,
    CONSTRAINT categories_type_check CHECK (((type)::text = ANY ((ARRAY['expense'::character varying, 'income'::character varying, 'both'::character varying])::text[])))
);


ALTER TABLE public.categories OWNER TO shinyjar;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO shinyjar;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    instagram_handle character varying(50),
    email character varying(100),
    phone character varying(20),
    address text,
    customer_since date DEFAULT CURRENT_DATE,
    total_spent numeric(10,2) DEFAULT 0.00,
    last_purchase date,
    notes text,
    business_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.customers OWNER TO shinyjar;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO shinyjar;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: inventory; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.inventory (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    category character varying(50),
    unit_cost numeric(10,2) NOT NULL,
    quantity integer DEFAULT 0,
    reorder_level integer DEFAULT 10,
    supplier_id integer,
    business_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.inventory OWNER TO shinyjar;

--
-- Name: inventory_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.inventory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventory_id_seq OWNER TO shinyjar;

--
-- Name: inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.inventory_id_seq OWNED BY public.inventory.id;


--
-- Name: suppliers; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.suppliers (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    contact_person character varying(100),
    email character varying(100),
    phone character varying(20),
    website character varying(200),
    address text,
    notes text,
    business_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.suppliers OWNER TO shinyjar;

--
-- Name: suppliers_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.suppliers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.suppliers_id_seq OWNER TO shinyjar;

--
-- Name: suppliers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.suppliers_id_seq OWNED BY public.suppliers.id;


--
-- Name: transaction_items; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.transaction_items (
    id integer NOT NULL,
    transaction_id integer,
    inventory_id integer,
    description character varying(200),
    quantity integer DEFAULT 1 NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    total_price numeric(10,2) GENERATED ALWAYS AS (((quantity)::numeric * unit_price)) STORED
);


ALTER TABLE public.transaction_items OWNER TO shinyjar;

--
-- Name: transaction_items_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.transaction_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_items_id_seq OWNER TO shinyjar;

--
-- Name: transaction_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.transaction_items_id_seq OWNED BY public.transaction_items.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    transaction_date date DEFAULT CURRENT_DATE NOT NULL,
    amount numeric(10,2) NOT NULL,
    type character varying(10) NOT NULL,
    category_id integer,
    description text,
    customer_id integer,
    supplier_id integer,
    user_id integer,
    business_id integer,
    payment_method character varying(20),
    reference_number character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT transactions_type_check CHECK (((type)::text = ANY ((ARRAY['expense'::character varying, 'income'::character varying])::text[])))
);


ALTER TABLE public.transactions OWNER TO shinyjar;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transactions_id_seq OWNER TO shinyjar;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: shinyjar
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    full_name character varying(100),
    hashed_password character varying(255) NOT NULL,
    is_active boolean DEFAULT true,
    role character varying(20) DEFAULT 'user'::character varying,
    business_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO shinyjar;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: shinyjar
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO shinyjar;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shinyjar
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: budgets id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.budgets ALTER COLUMN id SET DEFAULT nextval('public.budgets_id_seq'::regclass);


--
-- Name: businesses id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.businesses ALTER COLUMN id SET DEFAULT nextval('public.businesses_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: inventory id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.inventory ALTER COLUMN id SET DEFAULT nextval('public.inventory_id_seq'::regclass);


--
-- Name: suppliers id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.suppliers ALTER COLUMN id SET DEFAULT nextval('public.suppliers_id_seq'::regclass);


--
-- Name: transaction_items id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transaction_items ALTER COLUMN id SET DEFAULT nextval('public.transaction_items_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: budgets; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.budgets (id, name, category_id, amount, period, start_date, end_date, business_id, created_at) FROM stdin;
1	Monthly Materials Budget	1	1000.00	monthly	2024-12-01	2024-12-31	1	2025-12-29 13:21:51.872301
2	Monthly Marketing Budget	4	500.00	monthly	2024-12-01	2024-12-31	1	2025-12-29 13:21:51.872301
3	Monthly Packaging Budget	2	200.00	monthly	2024-12-01	2024-12-31	1	2025-12-29 13:21:51.872301
4	Quarterly Tools Budget	5	300.00	quarterly	2024-10-01	2024-12-31	1	2025-12-29 13:21:51.872301
5	Yearly Website Budget	6	1200.00	yearly	2024-01-01	2024-12-31	1	2025-12-29 13:21:51.872301
6	Christmass Presents Budget 2025	\N	200.00	monthly	2025-12-01	2025-12-31	\N	2025-12-30 04:48:26.675624
\.


--
-- Data for Name: businesses; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.businesses (id, name, instagram_handle, currency, created_at) FROM stdin;
1	Shiny Jar	shiny_jar	EUR	2025-12-29 13:21:49.198269
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.categories (id, name, type, color, business_id) FROM stdin;
1	Materials	expense	#EF4444	1
2	Packaging	expense	#3B82F6	1
3	Shipping	expense	#8B5CF6	1
4	Marketing	expense	#10B981	1
5	Tools & Equipment	expense	#F59E0B	1
6	Office Supplies	expense	#6366F1	1
7	Website & Hosting	expense	#EC4899	1
8	Professional Services	expense	#14B8A6	1
9	Necklaces	income	#10B981	1
10	Earrings	income	#3B82F6	1
11	Bracelets	income	#8B5CF6	1
12	Rings	income	#F59E0B	1
13	Custom Orders	income	#EC4899	1
14	Repairs	income	#14B8A6	1
15	Workshops	income	#84CC16	1
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.customers (id, name, instagram_handle, email, phone, address, customer_since, total_spent, last_purchase, notes, business_id, created_at) FROM stdin;
21	Arsjana Shehaj	@arsjana_jewelry	arsjana@email.com	+355 68 987 6543	Tirana, Albania	2023-12-15	1871.24	2024-12-08	\N	1	2025-12-30 05:18:40.647722
10	Liam Miller	liam_miller	liam.miller@email.com	+0001112222	\N	2023-10-10	0.00	2024-10-30	\N	1	2025-12-29 13:21:49.850184
11	Ava Davis	ava_davis	ava.davis@email.com	+1112223334	\N	2023-11-15	0.00	2024-10-25	\N	1	2025-12-29 13:21:49.850184
12	Ethan Wilson	ethan_wilson	ethan.wilson@email.com	+2223334445	\N	2023-12-20	0.00	2024-10-20	\N	1	2025-12-29 13:21:49.850184
13	Charlotte Moore	charlotte_moore	charlotte.moore@email.com	+3334445556	\N	2024-01-25	0.00	2024-10-15	\N	1	2025-12-29 13:21:49.850184
14	Benjamin Anderson	ben_anderson	benjamin.anderson@email.com	+4445556667	\N	2024-02-28	0.00	2024-10-10	\N	1	2025-12-29 13:21:49.850184
15	Amelia Thomas	amelia_thomas	amelia.thomas@email.com	+5556667778	\N	2024-03-15	0.00	2024-10-05	\N	1	2025-12-29 13:21:49.850184
16	James Jackson	james_jackson	james.jackson@email.com	+6667778889	\N	2024-04-20	0.00	2024-09-30	\N	1	2025-12-29 13:21:49.850184
17	Harper White	harper_white	harper.white@email.com	+7778889990	\N	2024-05-25	0.00	2024-09-25	\N	1	2025-12-29 13:21:49.850184
18	Lucas Harris	lucas_harris	lucas.harris@email.com	+8889990001	\N	2024-06-30	0.00	2024-09-20	\N	1	2025-12-29 13:21:49.850184
19	Evelyn Martin	evelyn_martin	evelyn.martin@email.com	+9990001112	\N	2024-07-05	0.00	2024-09-15	\N	1	2025-12-29 13:21:49.850184
20	Alexander Thompson	alex_thompson	alexander.thompson@email.com	+0001112223	\N	2024-08-10	0.00	2024-09-10	\N	1	2025-12-29 13:21:49.850184
2	Luca Rossi	luca_designs	luca.rossi@email.com	+2223334444	\N	2023-02-20	686.56	2024-12-05	\N	1	2025-12-29 13:21:49.850184
3	Sophie Chen	sophie_style	sophie.chen@email.com	+3334445555	\N	2023-03-10	1004.74	2024-12-01	\N	1	2025-12-29 13:21:49.850184
4	Marcus Lee	marcus_creates	marcus.lee@email.com	+4445556666	\N	2023-04-05	1542.89	2024-11-28	\N	1	2025-12-29 13:21:49.850184
1	Emma Johnson	emma_jewels	emma.johnson@email.com	+1112223333	\N	2023-01-15	2962.93	2024-12-10	\N	1	2025-12-29 13:21:49.850184
5	Isabella Garcia	bella_jewelry	isabella.garcia@email.com	+5556667777	\N	2023-05-12	973.39	2024-11-25	\N	1	2025-12-29 13:21:49.850184
6	Oliver Smith	oliver_smith	oliver.smith@email.com	+6667778888	\N	2023-06-18	1140.20	2024-11-20	\N	1	2025-12-29 13:21:49.850184
7	Chloe Williams	chloe_designs	chloe.williams@email.com	+7778889999	\N	2023-07-22	976.93	2024-11-15	\N	1	2025-12-29 13:21:49.850184
8	Noah Brown	noah_brown	noah.brown@email.com	+8889990000	\N	2023-08-30	733.24	2024-11-10	\N	1	2025-12-29 13:21:49.850184
9	Mia Taylor	mia_taylor	mia.taylor@email.com	+9990001111	\N	2023-09-05	1210.76	2024-11-05	\N	1	2025-12-29 13:21:49.850184
22	Maria Magdalena	@maria_magdalena	magdalena@shinyjar.com	\N	\N	2026-01-01	0.00	\N	\N	\N	2026-01-01 15:08:02.24546
\.


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.inventory (id, name, description, category, unit_cost, quantity, reorder_level, supplier_id, business_id, created_at, updated_at) FROM stdin;
1	Sterling Silver Chain	1mm sterling silver chain per meter	Materials	25.50	100	20	1	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
2	Gold-plated Earring Hooks	Gold-plated fishhook earrings	Materials	0.75	500	100	2	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
3	Swarovski Crystals	Assorted Swarovski crystals pack	Materials	45.00	50	10	3	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
4	Leather Cord	2mm black leather cord per meter	Materials	3.20	200	40	4	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
5	Freshwater Pearls	Assorted freshwater pearls	Materials	85.00	30	5	5	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
6	Amethyst Beads	6mm amethyst beads strand	Materials	32.00	40	8	6	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
7	Silver Clasps	Sterling silver lobster clasps	Materials	2.50	300	50	7	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
8	Jewelry Boxes	Small velvet jewelry boxes	Packaging	1.80	200	40	8	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
9	Pliers Set	Professional jewelry pliers set	Tools	45.00	10	2	9	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
10	Shipping Boxes	Small shipping boxes 10x10x5cm	Shipping	0.60	500	100	10	1	2025-12-29 13:21:49.966983	2025-12-29 13:21:49.966983
\.


--
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.suppliers (id, name, contact_person, email, phone, website, address, notes, business_id, created_at) FROM stdin;
2	Golden Beads Co.	Maria Garcia	maria@goldenbeads.com	+0987654321	goldenbeads.com	\N	\N	1	2025-12-29 13:21:49.570865
3	Crystal Palace	David Chen	david@crystalpalace.com	+1122334455	crystalpalace.com	\N	\N	1	2025-12-29 13:21:49.570865
4	Leather Crafts Ltd	Emma Wilson	emma@leathercrafts.com	+5566778899	leathercrafts.com	\N	\N	1	2025-12-29 13:21:49.570865
5	Pearl Paradise	Sophie Martin	sophie@pearlparadise.com	+6677889900	pearlparadise.com	\N	\N	1	2025-12-29 13:21:49.570865
6	Gemstone Wholesale	Michael Brown	michael@gemstone.com	+7788990011	gemstone.com	\N	\N	1	2025-12-29 13:21:49.570865
7	Metal Findings Corp	Lisa Taylor	lisa@metalfindings.com	+8899001122	metalfindings.com	\N	\N	1	2025-12-29 13:21:49.570865
8	Packaging Solutions	Robert Lee	robert@packaging.com	+9900112233	packagingsolutions.com	\N	\N	1	2025-12-29 13:21:49.570865
9	Tool Masters	Jennifer Wang	jennifer@toolmasters.com	+0011223344	toolmasters.com	\N	\N	1	2025-12-29 13:21:49.570865
10	Shipping Express	Thomas Anderson	thomas@shippingexpress.com	+2233445566	shippingexpress.com	\N	\N	1	2025-12-29 13:21:49.570865
11	Marketing Pros	Sarah Johnson	sarah@marketingpros.com	+3344556677	marketingpros.com	\N	\N	1	2025-12-29 13:21:49.570865
12	Web Services Inc	Kevin Davis	kevin@webservices.com	+4455667788	webservices.com	\N	\N	1	2025-12-29 13:21:49.570865
13	Accounting Plus	Amanda Clark	amanda@accountingplus.com	+5566778899	accountingplus.com	\N	\N	1	2025-12-29 13:21:49.570865
14	Legal Eagles	Daniel White	daniel@legaleagles.com	+6677889900	legaleagles.com	\N	\N	1	2025-12-29 13:21:49.570865
15	Insurance Partners	Jessica Hall	jessica@insurancepartners.com	+7788990011	insurancepartners.com	\N	\N	1	2025-12-29 13:21:49.570865
16	Cleaning Services	Brian King	brian@cleaning.com	+8899001122	cleaningservices.com	\N	\N	1	2025-12-29 13:21:49.570865
17	Utilities Co	Michelle Scott	michelle@utilities.com	+9900112233	utilitiesco.com	\N	\N	1	2025-12-29 13:21:49.570865
18	Rent Space Ltd	Christopher Young	chris@rentspace.com	+0011223344	rentspace.com	\N	\N	1	2025-12-29 13:21:49.570865
19	Software Solutions	Laura Allen	laura@softwaresolutions.com	+1122334455	softwaresolutions.com	\N	\N	1	2025-12-29 13:21:49.570865
20	Consulting Group	James Hernandez	james@consulting.com	+2233445566	consultinggroup.com	\N	\N	1	2025-12-29 13:21:49.570865
1	Silver World Inc.	Gerta Tirana	gerta@silverworld.com	+355 69 123 4567	silverworld.com	\N	\N	1	2025-12-29 13:21:49.570865
\.


--
-- Data for Name: transaction_items; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.transaction_items (id, transaction_id, inventory_id, description, quantity, unit_price) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.transactions (id, transaction_date, amount, type, category_id, description, customer_id, supplier_id, user_id, business_id, payment_method, reference_number, created_at, updated_at) FROM stdin;
6	2024-12-01	255.00	expense	1	Silver chains purchase	\N	1	1	1	card	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
7	2024-12-02	37.50	expense	1	Earring hooks	\N	2	1	1	paypal	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
8	2024-12-03	225.00	expense	1	Swarovski crystals	\N	3	1	1	bank_transfer	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
9	2024-12-04	64.00	expense	1	Leather cord	\N	4	1	1	card	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
10	2024-12-05	170.00	expense	1	Freshwater pearls	\N	5	1	1	card	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
11	2024-12-06	96.00	expense	2	Jewelry boxes	\N	8	1	1	paypal	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
12	2024-12-07	45.00	expense	5	New pliers set	\N	9	1	1	card	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
13	2024-12-08	30.00	expense	3	Shipping supplies	\N	10	1	1	cash	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
14	2024-12-09	150.00	expense	4	Instagram ads	\N	11	1	1	card	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
15	2024-12-10	99.99	expense	6	Website hosting	\N	12	1	1	card	\N	2025-12-29 13:21:50.146064	2025-12-29 13:21:50.146064
16	2024-12-08	220.00	income	9	Custom Silver Necklace with Sapphire	21	\N	\N	\N	card	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
17	2024-11-25	145.50	income	10	Gold Earrings Set	21	\N	\N	\N	paypal	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
18	2024-11-10	89.99	income	11	Leather Bracelet	21	\N	\N	\N	card	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
19	2024-10-15	320.00	income	13	Custom Wedding Ring Set	21	\N	\N	\N	bank_transfer	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
20	2024-09-28	75.25	income	12	Engraved Silver Ring	21	\N	\N	\N	card	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
21	2024-08-12	180.00	income	9	Pearl Necklace	21	\N	\N	\N	paypal	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
22	2024-07-05	450.00	income	13	Custom Diamond Earrings	21	\N	\N	\N	bank_transfer	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
23	2024-06-20	120.00	income	11	Crystal Bracelet Set	21	\N	\N	\N	card	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
24	2024-05-15	95.50	income	10	Silver Stud Earrings	21	\N	\N	\N	card	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
25	2024-04-10	175.00	income	9	Gold Chain Necklace	21	\N	\N	\N	paypal	\N	2025-12-30 05:23:41.866268	2025-12-30 05:23:41.866268
26	2024-12-05	850.00	expense	1	Silver Bars Purchase - Gerta Tirana	\N	1	\N	\N	bank_transfer	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
27	2024-11-20	450.00	expense	1	Gold Wire Order - Gerta Tirana	\N	1	\N	\N	card	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
28	2024-11-05	320.00	expense	1	Precious Stones - Gerta Tirana	\N	1	\N	\N	bank_transfer	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
29	2024-10-15	1250.00	expense	1	Bulk Silver Chains - Gerta Tirana	\N	1	\N	\N	bank_transfer	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
30	2024-09-28	680.00	expense	1	Gold Findings - Gerta Tirana	\N	1	\N	\N	card	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
31	2024-08-10	950.00	expense	1	Diamond Pieces - Gerta Tirana	\N	1	\N	\N	bank_transfer	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
32	2024-07-22	540.00	expense	1	Silver Sheets - Gerta Tirana	\N	1	\N	\N	card	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
33	2024-06-15	780.00	expense	1	Gold Chains - Gerta Tirana	\N	1	\N	\N	bank_transfer	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
34	2024-05-08	420.00	expense	1	Gemstones - Gerta Tirana	\N	1	\N	\N	card	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
35	2024-04-01	1150.00	expense	1	Platinum Wire - Gerta Tirana	\N	1	\N	\N	bank_transfer	\N	2025-12-30 05:27:18.254377	2025-12-30 05:27:18.254377
36	2025-12-08	220.00	income	9	Custom Silver Necklace with Sapphire	1	\N	\N	\N	card	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
37	2025-11-25	145.50	income	10	Gold Earrings Set	1	\N	\N	\N	paypal	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
38	2024-11-13	59.99	income	11	Leather Bracelet	1	\N	\N	\N	card	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
39	2024-10-15	240.00	income	13	Custom Wedding Ring Set	1	\N	\N	\N	bank_transfer	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
40	2024-09-12	75.25	income	12	Engraved Silver Ring	1	\N	\N	\N	card	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
41	2023-08-22	135.00	income	9	Pearl Necklace	1	\N	\N	\N	paypal	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
42	2023-07-05	350.00	income	13	Custom Diamond Earrings	1	\N	\N	\N	bank_transfer	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
43	2023-06-20	120.00	income	11	Crystal Bracelet Set	1	\N	\N	\N	card	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
44	2025-05-25	55.50	income	10	Silver Stud Earrings	1	\N	\N	\N	card	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
45	2024-04-11	275.00	income	9	Gold Chain Necklace	1	\N	\N	\N	stripe	\N	2026-01-01 11:33:44.098866	2026-01-01 11:33:44.098866
46	2024-09-13	191.01	income	10	Randomized Transaction	2	\N	\N	\N	bank_transfer	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
47	2024-09-23	251.82	income	13	Randomized Transaction	2	\N	\N	\N	card	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
48	2025-05-07	138.41	income	10	Randomized Transaction	2	\N	\N	\N	paypal	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
49	2024-12-15	105.32	income	12	Randomized Transaction	2	\N	\N	\N	bank_transfer	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
50	2025-12-28	23.76	income	11	Randomized Transaction	3	\N	\N	\N	paypal	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
51	2025-03-20	466.32	income	9	Randomized Transaction	3	\N	\N	\N	paypal	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
52	2024-12-16	436.07	income	9	Randomized Transaction	3	\N	\N	\N	paypal	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
53	2025-10-05	78.59	income	12	Randomized Transaction	3	\N	\N	\N	stripe	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
54	2025-03-01	302.10	income	9	Randomized Transaction	4	\N	\N	\N	stripe	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
55	2024-04-20	442.43	income	12	Randomized Transaction	4	\N	\N	\N	stripe	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
56	2024-04-26	413.64	income	12	Randomized Transaction	4	\N	\N	\N	paypal	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
57	2025-04-19	384.72	income	11	Randomized Transaction	4	\N	\N	\N	stripe	\N	2026-01-01 11:42:59.884676	2026-01-01 11:42:59.884676
58	2024-08-27	391.92	income	11	Randomized Transaction	1	\N	\N	\N	bank_transfer	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
59	2025-10-31	239.47	income	10	Randomized Transaction	5	\N	\N	\N	bank_transfer	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
60	2024-07-06	490.08	income	12	Randomized Transaction	6	\N	\N	\N	bank_transfer	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
61	2024-01-16	316.62	income	10	Randomized Transaction	7	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
62	2024-04-19	378.85	income	10	Randomized Transaction	8	\N	\N	\N	paypal	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
63	2025-07-12	481.20	income	13	Randomized Transaction	9	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
64	2024-05-25	231.72	income	13	Randomized Transaction	10	\N	\N	\N	paypal	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
65	2025-03-02	482.09	income	9	Randomized Transaction	1	\N	\N	\N	stripe	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
66	2025-02-01	370.95	income	13	Randomized Transaction	5	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
67	2024-09-25	157.45	income	11	Randomized Transaction	6	\N	\N	\N	paypal	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
68	2025-11-25	220.54	income	12	Randomized Transaction	7	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
69	2025-09-05	333.98	income	10	Randomized Transaction	8	\N	\N	\N	bank_transfer	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
70	2024-01-16	236.33	income	11	Randomized Transaction	9	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
71	2025-06-06	317.18	income	11	Randomized Transaction	10	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
72	2025-12-09	412.68	income	13	Randomized Transaction	1	\N	\N	\N	stripe	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
73	2025-01-24	362.97	income	12	Randomized Transaction	5	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
74	2024-12-23	492.67	income	9	Randomized Transaction	6	\N	\N	\N	bank_transfer	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
75	2025-10-17	439.77	income	13	Randomized Transaction	7	\N	\N	\N	paypal	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
76	2025-09-19	20.41	income	13	Randomized Transaction	8	\N	\N	\N	card	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
77	2024-01-31	493.23	income	11	Randomized Transaction	9	\N	\N	\N	paypal	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
78	2025-09-03	39.67	income	13	Randomized Transaction	10	\N	\N	\N	stripe	\N	2026-01-01 11:49:46.721957	2026-01-01 11:49:46.721957
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: shinyjar
--

COPY public.users (id, username, email, full_name, hashed_password, is_active, role, business_id, created_at) FROM stdin;
1	admin	admin@shinyjar.com	Admin User	$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW	t	admin	1	2025-12-29 13:21:49.237566
2	bora_malaj	bora@shinyjar.com	Bora Malaj	$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW	t	admin	1	2025-12-30 05:12:35.494943
3	gerta_tirana	gerta@silverworld.com	Gerta Tirana	$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW	t	supplier	1	2025-12-30 05:13:03.204572
4	arsjana_shehaj	arsjana@email.com	Arsjana Shehaj	$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW	t	customer	1	2025-12-30 05:13:29.117625
5	test_admin	test@shinyjar.com	Test Admin	$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW	t	admin	1	2025-12-30 12:24:59.856091
\.


--
-- Name: budgets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.budgets_id_seq', 6, true);


--
-- Name: businesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.businesses_id_seq', 1, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.categories_id_seq', 15, true);


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.customers_id_seq', 22, true);


--
-- Name: inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.inventory_id_seq', 10, true);


--
-- Name: suppliers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.suppliers_id_seq', 20, true);


--
-- Name: transaction_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.transaction_items_id_seq', 1, false);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.transactions_id_seq', 78, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shinyjar
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: budgets budgets_category_id_period_business_id_key; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_category_id_period_business_id_key UNIQUE (category_id, period, business_id);


--
-- Name: budgets budgets_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_pkey PRIMARY KEY (id);


--
-- Name: businesses businesses_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.businesses
    ADD CONSTRAINT businesses_pkey PRIMARY KEY (id);


--
-- Name: categories categories_name_business_id_key; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_business_id_key UNIQUE (name, business_id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- Name: transaction_items transaction_items_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transaction_items
    ADD CONSTRAINT transaction_items_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_customers_email; Type: INDEX; Schema: public; Owner: shinyjar
--

CREATE INDEX idx_customers_email ON public.customers USING btree (email);


--
-- Name: idx_customers_instagram; Type: INDEX; Schema: public; Owner: shinyjar
--

CREATE INDEX idx_customers_instagram ON public.customers USING btree (instagram_handle);


--
-- Name: idx_transactions_customer; Type: INDEX; Schema: public; Owner: shinyjar
--

CREATE INDEX idx_transactions_customer ON public.transactions USING btree (customer_id);


--
-- Name: idx_transactions_date; Type: INDEX; Schema: public; Owner: shinyjar
--

CREATE INDEX idx_transactions_date ON public.transactions USING btree (transaction_date);


--
-- Name: idx_transactions_supplier; Type: INDEX; Schema: public; Owner: shinyjar
--

CREATE INDEX idx_transactions_supplier ON public.transactions USING btree (supplier_id);


--
-- Name: idx_transactions_type; Type: INDEX; Schema: public; Owner: shinyjar
--

CREATE INDEX idx_transactions_type ON public.transactions USING btree (type);


--
-- Name: budgets budgets_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: budgets budgets_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: categories categories_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: customers customers_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: inventory inventory_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: inventory inventory_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id);


--
-- Name: suppliers suppliers_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: transaction_items transaction_items_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transaction_items
    ADD CONSTRAINT transaction_items_inventory_id_fkey FOREIGN KEY (inventory_id) REFERENCES public.inventory(id);


--
-- Name: transaction_items transaction_items_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transaction_items
    ADD CONSTRAINT transaction_items_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES public.transactions(id) ON DELETE CASCADE;


--
-- Name: transactions transactions_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: transactions transactions_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: transactions transactions_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: transactions transactions_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id);


--
-- Name: transactions transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shinyjar
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- PostgreSQL database dump complete
--

\unrestrict jkgmrlpaGepZoxXohocos1y0VwBN91KG9g5hI93QqmMmAJn6hgTuGEfREzan3OU

