create table locality
(id number,
name varchar2(200),
region varchar(10),
city varchar2(20)
)
PARTITION BY LIST (region) (  
       PARTITION ET VALUES ('east'), 
       PARTITION WT VALUES ('west'), 
       PARTITION NH VALUES ('north'),
	   PARTITION SH VALUES ('south'),
	   PARTITION CL VALUES ('central')
);


--Contains details of property
CREATE TABLE property_detail
(
   source              varchar2 (100),
   heading             VARCHAR2 (2000),
   location            VARCHAR2 (2000),
   super_buildup       VARCHAR2 (2000),
   price               VARCHAR2 (2000),
   description         VARCHAR2 (2000),
   society             VARCHAR2 (2000),
   features            VARCHAR2 (2000),
   floor_info          VARCHAR2 (2000),
   property_age        VARCHAR2 (2000),
   property_type       VARCHAR2 (2000),
   owner_dealer        VARCHAR2 (2000),
   owner_dealer_name   VARCHAR2 (2000),
   posted_date         VARCHAR2 (2000),
   map                 VARCHAR2 (2000)
)
