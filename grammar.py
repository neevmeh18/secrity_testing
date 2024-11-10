# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.
from fuzzingbook.GrammarFuzzer import is_valid_grammar
from fuzzingbook.Grammars import opts
import random 

d = {}
c_table_name = ''
table_just_created = ''
flag = 0
pk = 0
prev_table_names = ["contacts"]
def first_check(stmt):
    global d
    if flag > 1:
        return stmt
    else:
        d = {"contacts": ["contact_id", "first_name", "last_name", "email", "phone"]}
        return "CREATE TABLE contacts (contact_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, phone TEXT NOT NULL UNIQUE);"

def change_flag():
    global flag
    flag += 1

def drop_table(name):
    global d
    global prev_table_names
    d.pop(name, None)
    prev_table_names = list(d.keys())
    return 
    
def add_table_name(name):
    global d
    global flag
    global table_just_created
    global pk
    global c_table_name
    global prev_table_names
    pk =0
    prev_table_names = list(d.keys())
    if flag > 1:
        c_table_name = name
        d[name] = []
        table_just_created = name
    return 

def add_column_name(name):
    global d
    global table_just_created 
    try:
        d[table_just_created].append(name)
    except:
        pass
    return 


def get_table_name():
    global d
    global c_table_name
    global prev_table_names
    table_names = prev_table_names
    if table_names:

        c_table_name =  str(random.choice(table_names))
        return c_table_name
    else: 
        return "anywaynotgonnaexecute"


def get_table_and_column_name():
    global d
    global c_table_name

    try:
        column_names = d[c_table_name]
        return c_table_name + "." + str(random.choice(column_names))

    except:
        return "neev.notablefound"


def get_column_name():
    global d
    global c_table_name

    try:
        column_names = d[c_table_name]
        return str(random.choice(column_names))

    except:
        return "notablefound"

def pk_flag():
    global pk
    pk = 1
    return

def rowid_setter():
    global pk
    if pk ==1:
        return "" #rowid removed as errors were too many
    else:
        ""
def remove_temp_tables(temp, x, table_name, z):
    global d
    if temp == "":
        return 
    else:
        d.pop(table_name, None)
    

grammar = {"<start>": [("<sql_statement>;", opts(pre=change_flag, post=lambda sql_statement: first_check(sql_statement)))],
            "<sql_statement>": ["<create_table_simple>", "<create_table_simple>", "<select_stmt>", "<select_stmt>","<select_stmt>", "<create_table>", "<select_stmt>", "<create_table>", "<create_table>", "<create_view>", "<alter_table_stmt>", "<create_index_stmt>", "<drop_table_stmt>", "<pragma_stmt>", "<pragma_stmt>", "<drop_index_stmt>", "<drop_view_stmt>"],

            ## PRAGMA STATEMENTS
           
            "<pragma_stmt>": ["PRAGMA <pragma_stuff>"],
            "<pragma_stuff>": ["<pragma_empty>", "<pragma_boolean>"],
            "<pragma_empty>": ["analysis_limit", "application_id", "auto_vacuum", "automatic_index", "busy_timeout", "cache_size", "cache_spill", "cell_size_check", "checkpoint_fullfsync", "collation_list", "compile_options", "count_changes", "data_store_directory", "data_version", "database_list", "default_cache_size", "defer_foreign_keys", "empty_result_callbacks", "encoding", "foreign_key_check", "foreign_keys", "freelist_count", "full_column_names", "fullfsync", "function_list", "hard_heap_limit", "incremental_vacuum", "integrity_check", "journal_mode", "journal_size_limit", "legacy_alter_table", "legacy_file_format", "locking_mode", "max_page_count", "mmap_size", "module_list", "optimize", "page_count", "page_size", "pragma_list", "query_only", "quick_check", "read_uncommitted", "recursive_triggers", "reverse_unordered_selects", "schema_version", "secure_delete", "short_column_names", "shrink_memory", "soft_heap_limit", "stats", "synchronous", "table_list", "temp_store", "temp_store_directory", "threads", "trusted_schema", "user_version", "wal_autocheckpoint", "writable_schema=RESET"],
            "<pragma_boolean>": ["<pragma_b_name> = <boolean_values>"],
            "<boolean_values>": ["0", "1", "yes", "true", "on", "no", "false", "off"],
            "<pragma_b_name>": ["automatic_index", "cache_spill", "case_sensitive_like", "cell_size_check", "checkpoint_fullfsync", "count_changes", "defer_foreign_keys", "empty_result_callbacks", "foreign_keys", "full_column_names", "fullfsync", "ignore_check_constraints", "legacy_alter_table", "parser_trace", "query_only", "read_uncommitted", "recursive_triggers", "reverse_unordered_selects", "secure_delete", "short_column_names", "trusted_schema", "vdbe_addoptrace", "vdbe_debug", "vdbe_listing", "vdbe_trace", "writable_schema"],


            ## EXPR

           "<expr>": ["<literal_value>", "<bind_parameter>", ("<table_name>.<column_name>", opts(pre=get_table_and_column_name)), "<unary_operator> <expr>", "(<expressions>)", "CAST(<expr> AS <data_type>)", "<expr> COLLATE <collation_name>", "<expr> <not> <expr_stuff1>", "<expr> <expr_stuff2>", "<expr> IS <not> <distinct_from> <expr>", "<expr> <not> BETWEEN <expr> AND <expr>", "<expr> <not> IN <expr_stuff3>", "<not_exists> (<select_stmt>)", "CASE <expr_maybe> <when_clauses> <else_clause> END"],       
            "<literal_value>": ["<numeric_literal>", "<string_literal>", "<blob_literal>", "NULL", "TRUE", "FALSE", "CURRENT_TIME", "CURRENT_DATE", "CURRENT_TIMESTAMP"],
            "<numeric_literal>": ["<integer><e_value>", "<integer>.<integer><e_value>", ".<integer><e_value>", "0x<hexnumber>"],
            "<e_value>": ["", "E<signed_number>", "e<signed_number>"],
            "<string_literal>": ["<string>"],
            "<blob_literal>": ["0x<hexnumber>"],
            "<bind_parameter>": ["NULL"],
            "<unary_operator>": ["+", "-", "~"],
            "<not>": ["", "NOT"],
            "<expr_stuff1>": ["LIKE <expr> <escape_expr>", "GLOB <expr>", "REGEXP <expr>", "MATCH <expr>"],
            "<escape_expr>": ["", "ESCAPE <expr>"],
            "<expr_stuff2>": ["ISNULL", "NOTNULL", "NOT NULL"],
            "<distinct_from>": ["", "DISTINCT FROM"],
            "<expr_stuff3>": ["(<expr_stuff4>)", "<table_name>"],
            "<expr_stuff4>": ["", "<select_stmt>", "<expressions>"],
            "<not_exists>": ["", "EXISTS", "NOT EXISTS"],
            "<when_clauses>": ["<when_clause>", "<when_clauses> <when_clause>"],
            "<when_clause>": ["WHEN <expr> THEN <expr>"],
            "<else_clause>": ["", "ELSE <expr>"],
            #"<raise_function>": ["RAISE (<raise_function_stuff>)"],
            #"<raise_function_stuff>": ["IGNORE", "ROLLBACK, <string>", "ABORT, <string>", "FAIL, <string>"],
  
            

            ## SELECT STATEMENT

           "<select_stmt>": ["<select_clause>"],
           
            
            "<select_clause>": ["SELECT <select_clause_stuff1> <result_columns> <from_clause> <where_clause> <group_by_clause> <having_clause> "], #select empty removed
            "<select_clause_stuff1>": ["", "DISTINCT", "ALL"],
            "<result_columns>": ["<result_column>", "<result_columns>,<result_column>"],
            "<result_column>": ["<expr> <result_column_stuff>", "*", "<table_name>.*"],
            "<result_column_stuff>": ["", "AS <column_alias>", "<column_alias>"],
            "<column_alias>": ["<identifier>"],

            "<from_clause>": ["FROM <table_name>"],
           
            "<where_clause>": ["", "WHERE <expr>"],
           
            "<group_by_clause>": ["", "GROUP BY <expressions>"],
            "<expressions>": ["<expr>", "<expr>,<expr>"],
           
            "<having_clause>": ["", "HAVING <aggregate_function_invocation> <having_clause_stuff> <signed_number>"],
            "<having_clause_stuff>": ["=", ">", "<"],
            "<aggregate_function_invocation>": ["<aggregate_func> <filter_clause>"],
            "<aggregate_func>": ["avg(<expr>)", "count(<expr>)", "min(<expr>)", "sum(<expr>)", "total(<expr>)", "count(*)", "count(<expr>)", "group_concat(<expr>)", "max(<expr>)"],
            "<filter_clause>": [""],

           





            "<collation_name>": ["BINARY", "NOCASE", "RTRIM"],
           
            "<expr_maybe>": ["<expr>", ""],
            "<expressions>": ["<expr>", "<expr>,<expr>"],
            "<column_name>": [("<identifier>", opts(pre=get_column_name))],
            "<type>": ["INTEGER", "TEXT", "REAL", "BLOB", "NUMERIC"],
            "<size>": ["<signed_number>", "<signed_number>,<signed_number>"],

            "<table_name>": [("<identifier>", opts(pre=get_table_name))],

            ##CREATE VIEW STATEMENTS
            "<create_view>": ["CREATE <temp> VIEW <if_not_exists> <identifier> <create_view_stuff> AS <select_stmt>"],
            "<create_view_stuff>": ["", "(<column_names>)"],

            ##DROP VIEW STATEMENTS
            "<drop_view_stmt>": ["DROP VIEW IF EXISTS <identifier>"],

            ##CREATE INDEX STATEMENT

            "<create_index_stmt>": ["CREATE <unique> INDEX <if_not_exists> <identifier> ON <table_name> (<indexed_columns>) <where_clause>"],
            "<unique>": ["", "", "UNIQUE"],

           ##DROP INDEX 

            "<drop_index_stmt>": ["DROP INDEX IF EXISTS <identifier>"],
           
            ##DROP TABLE 

            "<drop_table_stmt>": [("DROP TABLE IF EXISTS <table_name>", opts(post=lambda table_name: drop_table(table_name)))],

            ##CREATE SIMPLE 

            "<create_table_simple>": ["CREATE TABLE IF NOT EXISTS <create_table_name> (<table_columns_def>)"],

           
            ##CREATE TABLE STATEMENT
            "<create_table>": [("CREATE <temp> TABLE <if_not_exists> <identifier> <create_table_stuff>", opts(post=lambda temp, x, table_name, z: remove_temp_tables(temp, x, table_name, z)))],
            "<temp>": ["", "", "", "", "", "", "TEMP", "TEMPORARY"],
            "<create_table_stuff>": ["AS <select_stmt>", "(<table_columns_def>, <table_constraints>) <table_options>"], 
            "<if_not_exists>": ["IF NOT EXISTS", ""],
            #"<if_exists>": ["IF EXISTS", ""],
            "<table_constraints>": ["<table_constraint>", "<table_constraints>,<table_constraint>"],
            "<table_constraint>": ["<constraint_name> <table_constraint_body>"],
            "<table_constraint_body>": [("PRIMARY KEY (<indexed_columns>) <conflict_clause>", opts(pre=pk_flag)), "UNIQUE (<indexed_columns>) <conflict_clause>", "CHECK (<expr>)"], #"FOREIGN KEY (<column_names>) <foreign_key_clause>"],
            "<indexed_columns>": ["<indexed_column>", "<indexed_columns>, <indexed_column>"],
            "<indexed_column>": ["<column_name> <ordering_term_stuff1> <ordering>"],
            "<table_options>": ["", "<table_option>", "<table_options><table_option>"],
            "<table_option>": [""], # removed strict as datatypes did not match and rowid
            "<create_table_name>": [("<identifier>", opts(post = lambda identifier: add_table_name(identifier)))],
            "<table_name>": [("<identifier>", opts(pre=get_table_name))],
            "<table_columns_def>": ["<table_column_def>", "<table_columns_def>,<table_column_def>"],
            "<table_column_def>": ["<create_column_name> <data_type> <column_constraint>"],
            "<create_column_name>": [("<identifier>", opts(post = lambda identifier: add_column_name(identifier)))],
            "<column_constraint>": ["<constraint>", "<column_constraint> <constraint>"],
            "<constraint>": ["<constraint_name> <constraint_body>"],
            "<constraint_name>": ["", "CONSTRAINT <identifier>"],
            "<constraint_body>": ["PRIMARY KEY <ordering> <conflict_clause> <autoincrement>", "NOT NULL <conflict_clause>", "UNIQUE <conflict_clause>", "CHECK(<expr>)", "DEFAULT <default_clause>", "COLLATE <collation_name>", "<foreign_key_clause>", "<generated_always> AS(<expr>) <stored_virtual>"],
            "<generated_always>": ["", "GENERATED ALWAYS"],
            "<stored_virtual>": ["", "STORED", "VIRTUAL"],
            "<collation_name>": ["BINARY", "NOCASE", "RTRIM"], 
            "<ordering>": ["", "ASC", "DESC"],
            "<conflict_clause>": ["", "ON CONFLICT <conflict_action>"],
            "<conflict_action>": ["ROLLBACK", "ABORT", "FAIL", "IGNORE", "REPLACE"],
            "<autoincrement>": ["", "AUTOINCREMENT"],
            "<default_clause>": [" <expr>", " <literal_value>", " <signed_number>"],
            "<ordering_term_stuff1>": ["", "COLLATE <collation_name>"],
            "<foreign_key_clause>": [""],
            "<column_names>": ["<column_name>", "<column_names>,<column_name>"],

            ##Alter table

            "<alter_table_stmt>": ["ALTER TABLE <table_name> <alter_table_stuff>"],
            "<alter_table_stuff>": ["RENAME TO <create_table_name>", "RENAME COLUMN <column_name> to <create_column_name>", "ADD COLUMN <table_column_def>", "DROP COLUMN <column_name>", "RENAME <column_name> to <create_column_name>", "ADD <table_column_def>", "DROP <column_name>"],



           
            "<data_type>": ["<type>", "<type>(<size>)", ""],
            #"<size>": ["<signed_number>", "<signed_number>,<signed_number>"],
            "<signed_number>": ["-<integer>", "+<integer>", "<integer>"],
            "<integer>": ["<digit>", "<integer><digit>"],
            "<hexnumber>": ["<hexdigit>", "<hexnumber><hexdigit>"],
            "<identifier>": ["<letter>", "<identifier><letter>", "<identifier><digit>"],
            "<string>": ["<letter>", "<digit>", "<string><letter>", "<string><digit>"],
            "<hexdigit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"],
            "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
           }
          

