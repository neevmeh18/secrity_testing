# Grammar based Fuzzer for SQLite
This project implements a grammar-based blackbox fuzzer to test SQLite, generating diverse SQL commands to maximize code coverage and identify potential bugs. The fuzzer runs within a Dockerized Ubuntu environment, ensuring consistency across platforms. Key files include grammar.py, which defines the SQL grammar, and fuzzer.py, which handles input generation.
