CREATE TABLE IF NOT EXISTS test (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

INSERT INTO test (name) VALUES ('Alice'), ('Bob'), ('Charlie'), ('Diana'), ('Eve');