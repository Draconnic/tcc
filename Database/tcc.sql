--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

---
--- drop SCHEMA
---

DROP SCHEMA IF EXISTS finetornos;

---
--- create SCHEMA 
---

CREATE SCHEMA finetornos;

---
--- drop tables
---

DROP TABLE IF EXISTS finetornos.devices;
DROP TABLE IF EXISTS finetornos.records;
DROP TABLE IF EXISTS finetornos.measurement;

--
-- Name: devices; Type: TABLE; Schema: finetornos; Owner: -; Tablespace: 
--

CREATE TABLE finetornos.devices (
    chip_id varchar(20) NOT NULL UNIQUE,
    machine_id varchar(20) NOT NULL UNIQUE,
    updated timestamp DEFAULT NOW()
); 


--
-- Name: records; Type: TABLE; Schema: finetornos; Owner: -; Tablespace: 
--

CREATE TABLE finetornos.records (
    created timestamp,
    chip_id varchar,
    current_machine varchar,
    previous_machine varchar
);

--
-- Name: measurement; Type: TABLE; Schema: finetornos; Owner: -; Tablespace: 
--

CREATE TABLE finetornos.measurement (
    chip_id varchar(20) NOT NULL,
    bubbler_state BOOLEAN NOT NULL,
    level_sensor_connection BOOLEAN NOT NULL,
    level_sensor_state BOOLEAN NOT NULL,
    ph_sensor_value FLOAT NOT NULL,
    skimmer_state BOOLEAN NOT NULL,
    date_time timestamp NOT NULL
);


SET search_path TO finetornos, public;

--
-- Name: recorder(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE OR REPLACE FUNCTION finetornos.recorder()
    RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR (TG_OP = 'UPDATE' AND NEW.machine_id <> OLD.machine_id) THEN
        INSERT INTO finetornos.records (created, chip_id, current_machine, previous_machine)
        VALUES (NOW(), NEW.chip_id, NEW.machine_id, OLD.machine_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--
-- Name: devices_trigger; Type: TRIGGER; Schema: finetornos; Owner: -
--

CREATE TRIGGER devices_trigger
    AFTER INSERT OR UPDATE ON finetornos.devices
    FOR EACH ROW
    EXECUTE FUNCTION finetornos.recorder();

--
-- Name: pk_devices; Type: CONSTRAINT; Schema: finetornos; Owner: -
--

ALTER TABLE ONLY finetornos.devices
    ADD CONSTRAINT pk_devices PRIMARY KEY (chip_id);

--
-- Name: pk_records; Type: CONSTRAINT; Schema: finetornos; Owner: -
--

ALTER TABLE ONLY finetornos.records
    ADD CONSTRAINT pk_records FOREIGN KEY (chip_id) REFERENCES finetornos.devices(chip_id);

--
-- Name: fk_measurement_devices; Type: CONSTRAINT; Schema: finetornos; Owner: -
--

ALTER TABLE ONLY finetornos.measurement
    ADD CONSTRAINT fk_measurement_devices FOREIGN KEY (chip_id) REFERENCES finetornos.devices(chip_id);

--
-- Name: fk_measurement_devices; Type: CONSTRAINT; Schema: finetornos; Owner: -
--

ALTER TABLE ONLY finetornos.measurement
    ALTER COLUMN date_time SET DEFAULT DATE_TRUNC('minute', NOW());

