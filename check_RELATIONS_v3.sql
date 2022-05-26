CREATE TABLE yelp_business (

	business_id VARCHAR PRIMARY KEY,

	name VARCHAR,-- (30),

	address VARCHAR,-- (30),

	city VARCHAR,-- (10),

	state CHAR(2),--VARCHAR (2),

	postal_code CHAR (5),

	latitude double precision,--CHAR (10), --double

	longitude double precision,--CHAR (10),

	stars REAL,--CHAR(2), -- real number

	--review_count INT,--CHAR(4),

	is_open INT,--CHAR(5), --bool

	numCheckins INT,

	numTips INT

	--attributes VARCHAR (1000),

	--category VARCHAR(100),

	--hours TIMESTAMP (6)

);

CREATE TABLE yelp_user (

	user_id VARCHAR PRIMARY KEY,

	cool INT,--CHAR(5),

	fans INT,--CHAR(3),

	--friends VARCHAR(100),

	funny INT,--CHAR (3),

	name VARCHAR,-- (20),

	tipcount INT,--CHAR (3),

	useful INT,--VCHAR (4),

	yelping_since TIMESTAMP,-- (6),

	user_latitude double precision,

	user_longitude double precision,

	totalLikes INT,

	average_stars REAL

);

--TABLE yelp_tips ms2 edit
CREATE TABLE yelp_tips (

	user_id VARCHAR,--CHAR (5),

	business_id VARCHAR,--VARCHAR (15),

	date TIMESTAMP,-- (6),

	likes INT,--CHAR (2),

	text VARCHAR,-- (100),

	PRIMARY KEY (user_id, business_id, date),

	FOREIGN KEY (business_id) REFERENCES yelp_business (business_id),

	FOREIGN KEY (user_id) REFERENCES yelp_user (user_id)

);

--total participation of business in tips relation cant be enforced

--TABLE friends ms2 new added
CREATE TABLE friends(
	user_id_1 VARCHAR,
	user_id_2 VARCHAR,
	PRIMARY KEY(user_id_1,user_id_2),
	FOREIGN KEY(user_id_1) REFERENCES yelp_user(user_id),
	FOREIGN KEY(user_id_2) REFERENCES yelp_user(user_id)
);

--TABLE checkin ms2 new added
CREATE TABLE checkins(
	business_id VARCHAR,
	checkin_time TIMESTAMP,
	--year INT
	--month INT
	--day INT
	PRIMARY KEY(business_id, checkin_time),
	FOREIGN KEY(business_id) REFERENCES yelp_business(business_id)
);

--TABLE attributes ms2 new added
CREATE TABLE attributes(
	business_id VARCHAR,
	attr_name VARCHAR,
	value VARCHAR,
	PRIMARY KEY(business_id, attr_name),
	FOREIGN KEY(business_id) REFERENCES yelp_business(business_id)
);

--TABLE categories ms2 new added
CREATE TABLE categories(
	business_id VARCHAR,
	category_name VARCHAR,
	PRIMARY KEY(business_id,category_name),
	FOREIGN KEY(business_id) REFERENCES yelp_business(business_id)
);

--TABLE hours ms2 new added
CREATE TABLE hours(
	business_id VARCHAR,
	dayofweek VARCHAR,
	open TIME,
	close TIME,
	PRIMARY KEY(business_id,dayofweek),
	FOREIGN KEY(business_id) REFERENCES yelp_business(business_id)
);