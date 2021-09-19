/* 이름: demo_madang.sql */
/* 설명 */
 
/* root 계정으로 접속, madang 데이터베이스 생성, madang 계정 생성 */
/* MySQL Workbench에서 초기화면에서 +를 눌러 root connection을 만들어 접속한다. */
DROP DATABASE IF EXISTS  loading_DB;
DROP USER IF EXISTS  loading_DB@localhost;
create user loading_DB@localhost identified WITH mysql_native_password  by 'loding';
create database loading_DB;
grant all privileges on loading_DB.* to loading_DB@localhost with grant option;
commit;

/* madang DB 자료 생성 */
/* 이후 실습은 MySQL Workbench에서 초기화면에서 +를 눌러 madang connection을 만들어 접속하여 사용한다. */
 
USE loading_DB;

CREATE TABLE WORKER(
    WORKER_TASK VARCHAR(8) NOT NULL,
    WORKER_DATE DATE NOT NULL,
    WORKER_PERSONNEL INT NOT NULL
);

CREATE TABLE LOGIN(
    LI_PHONENUM VARCHAR(10) NOT NULL,
    LI_NAME VARCHAR(20) NOT NULL,
    LI_UNLOADING VARCHAR(30) NOT NULL,
    IP VARCHAR(20) NOT NULL,
    HOLD INT,
    DECK INT,
    VESSEL_NAME VARCHAR(30),
    F_S VARCHAR(5)
);

CREATE TABLE SCHEDULE(
    SCHEDULE_IMPORT TIMESTAMP(0) NOT NULL,
    SCHEDULE_EXPORT TIMESTAMP(0) NOT NULL,
    VESSEL_NAME VARCHAR(30) NOT NULL,
    SCHEDULE_TON INT NOT NULL
);

CREATE TABLE VESSEL(
    VESSEL_NAME VARCHAR(30) NOT NULL,
    VESSEL_MRN VARCHAR(15) NOT NULL,
    VESSEL_TON INT NOT NULL,
    VESSEL_TYPE VARCHAR(15) NOT NULL
);

CREATE TABLE DECK(
    DECK_TON INT NOT NULL,
    DECK_FLOOR VARCHAR(2) NOT NULL,
    VESSEL_NAME VARCHAR(30) NOT NULL,
    HOLD_NO VARCHAR(2) NOT NULL
);

CREATE TABLE CARGO(
    CARGO_VIN VARCHAR(20) NOT NULL,
    VESSEL_NAME VARCHAR(30) NOT NULL,
    CARGO_NAME VARCHAR(30) NOT NULL,
    CARGO_WEIGHT INT NOT NULL,
    CARGO_INSPECT_TIME TIMESTAMP(0) NOT NULL,
    IP VARCHAR(20) NOT NULL,
    LI_PHONENUM VARCHAR(10) NOT NULL,
    DECK INT NOT NULL,
    HOLD INT NOT NULL
);

CREATE TABLE CAR(
    CAR_NAME VARCHAR(15) NOT NULL,
    CAR_WEIGHT INT NOT NULL
);

CREATE TABLE STORAGE(
    CARGO_VIN VARCHAR(20) NOT NULL,
    CARGO_NAME VARCHAR(30) NOT NULL,
    INSPECT_TIME TIMESTAMP(0) NOT NULL,
    IP VARCHAR(20) NOT NULL,
    LI_PHONENUM VARCHAR(10) NOT NULL
);

CREATE TABLE IMAGE(
	IMAGE_NAME VARCHAR(25) NOT NULL,
    IMAGE LONGBLOB NOT NULL
) ;

CREATE TABLE TEMP(
	IMAGE_NAME VARCHAR(25) NOT NULL,
    IMAGE LONGBLOB NOT NULL
) ;

ALTER TABLE WORKER ADD CONSTRAINT PK_WORKER PRIMARY KEY (WORKER_TASK);
ALTER TABLE LOGIN ADD CONSTRAINT PK_LOGIN PRIMARY KEY (IP);
ALTER TABLE SCHEDULE ADD CONSTRAINT PK_SCHEDULE PRIMARY KEY (SCHEDULE_IMPORT, VESSEL_NAME);
ALTER TABLE VESSEL ADD CONSTRAINT PK_VESSEL PRIMARY KEY (VESSEL_NAME);
ALTER TABLE DECK ADD CONSTRAINT PK_DECK PRIMARY KEY (DECK_TON,DECK_FLOOR,VESSEL_NAME);
ALTER TABLE CARGO ADD CONSTRAINT PK_CARGO PRIMARY KEY (CARGO_VIN);
ALTER TABLE CAR ADD CONSTRAINT PK_CAR PRIMARY KEY (CAR_NAME);
ALTER TABLE STORAGE ADD CONSTRAINT PK_STORAGE PRIMARY KEY (CARGO_VIN);
ALTER TABLE IMAGE ADD CONSTRAINT PK_IMAGE PRIMARY KEY (IMAGE_NAME) ;
ALTER TABLE TEMP ADD CONSTRAINT PK_IMAGE PRIMARY KEY (IMAGE_NAME) ;

ALTER TABLE LOGIN ADD CONSTRAINT FK_VESSEL0 FOREIGN KEY (VESSEL_NAME) REFERENCES VESSEL(VESSEL_NAME);
ALTER TABLE DECK ADD CONSTRAINT FK_VESSEL1 FOREIGN KEY (VESSEL_NAME) REFERENCES VESSEL(VESSEL_NAME);
ALTER TABLE SCHEDULE ADD CONSTRAINT FK_VESSEL2 FOREIGN KEY (VESSEL_NAME) REFERENCES VESSEL(VESSEL_NAME);
ALTER TABLE CARGO ADD CONSTRAINT FK_VESSEL3 FOREIGN KEY (VESSEL_NAME) REFERENCES VESSEL(VESSEL_NAME);
ALTER TABLE CARGO ADD CONSTRAINT FK_CAR1 FOREIGN KEY (CARGO_NAME) REFERENCES CAR(CAR_NAME);

INSERT INTO CAR VALUES('santafe',1778);
INSERT INTO CAR VALUES('g90',2098);
INSERT INTO CAR VALUES('i30',1297);
INSERT INTO CAR VALUES('tussan',1595);
INSERT INTO CAR VALUES('kona',1375);
INSERT INTO CAR VALUES('sonata',1440);
INSERT INTO CAR VALUES('porter2',1859);
INSERT INTO CAR VALUES('avante',1254);
INSERT INTO CAR VALUES('i30',1297);
INSERT INTO CAR VALUES('veloster',1285);
INSERT INTO CAR VALUES('palisade',1956);
INSERT INTO CAR VALUES('venue',1197);
INSERT INTO CAR VALUES('g70',1676);
INSERT INTO CAR VALUES('g80',1822);
INSERT INTO CAR VALUES('gv80',2090);
INSERT INTO CAR VALUES('starex',2177);
INSERT INTO CAR VALUES('ioniq',1380);
INSERT INTO CAR VALUES('nexo',1852);