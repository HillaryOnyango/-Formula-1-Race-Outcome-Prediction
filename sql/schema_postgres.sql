CREATE TABLE IF NOT EXISTS drivers (
    driver_id TEXT PRIMARY KEY,
    code TEXT,
    given_name TEXT,
    family_name TEXT,
    nationality TEXT
);

CREATE TABLE IF NOT EXISTS constructors (
    constructor_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    nationality TEXT
);

CREATE TABLE IF NOT EXISTS races (
    race_id TEXT PRIMARY KEY,
    season INT NOT NULL,
    round INT NOT NULL,
    race_name TEXT NOT NULL,
    circuit_id TEXT,
    race_date DATE,
    UNIQUE (season, round)
);

CREATE TABLE IF NOT EXISTS results (
    result_id BIGSERIAL PRIMARY KEY,
    race_id TEXT REFERENCES races(race_id),
    driver_id TEXT REFERENCES drivers(driver_id),
    constructor_id TEXT REFERENCES constructors(constructor_id),
    grid INT,
    finish_position INT,
    points NUMERIC,
    status TEXT,
    UNIQUE (race_id, driver_id)
);

CREATE TABLE IF NOT EXISTS lap_times (
    lap_time_id BIGSERIAL PRIMARY KEY,
    race_id TEXT REFERENCES races(race_id),
    driver_id TEXT REFERENCES drivers(driver_id),
    lap_number INT,
    lap_time_ms INT,
    sector1_ms INT,
    sector2_ms INT,
    sector3_ms INT,
    UNIQUE (race_id, driver_id, lap_number)
);

CREATE TABLE IF NOT EXISTS telemetry (
    telemetry_id BIGSERIAL PRIMARY KEY,
    race_id TEXT REFERENCES races(race_id),
    driver_id TEXT REFERENCES drivers(driver_id),
    sample_ts TIMESTAMPTZ,
    speed NUMERIC,
    throttle NUMERIC,
    brake NUMERIC,
    drs INT,
    gear INT,
    rpm INT
);
