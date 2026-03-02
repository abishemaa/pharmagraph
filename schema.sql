CREATE TABLE drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    drug_class TEXT,
    notes TEXT
);

CREATE TABLE interactions (
    drug_a_id INTEGER NOT NULL,
    drug_b_id INTEGER NOT NULL,
    severity TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    PRIMARY KEY (drug_a_id, drug_b_id),
    CHECK (drug_a_id < drug_b_id),
    FOREIGN KEY (drug_a_id) REFERENCES drugs(id),
    FOREIGN KEY (drug_b_id) REFERENCES drugs(id)
);