import duckdb
import sys
import os




def table_cadastro(duckPath):
   con=duckdb.connect(database=duckPath, read_only=False)
   con.sql(f"CREATE TABLE CADASTRO (EMAIL VARCHAR PRIMARY KEY,NOME VARCHAR,SENHA VARCHAR)")
   con.close()




def novo_cadastro(duckPath,EMAIL,NOME,SENHA):
   con=duckdb.connect(database=duckPath, read_only=False)
   con.sql(f"INSERT INTO CADASTRO(EMAIL,NOME,SENHA) VALUES ('{EMAIL}','{NOME}','{SENHA}')")
   con.close


def excluir_cadastro(duckPath,EMAIL):
	con=duckdb.connect(database=duckPath, read_only=False)
	con.sql(f"DELETE FROM CADASTRO WHERE EMAIL='{EMAIL}'")


if __name__ == "__main__":
   EMAIL = sys.argv[1]
   NOME = sys.argv[2]
   SENHA = sys.argv[3]
   duckPath=f'~/database/database'
   novo_cadastro(duckPath,EMAIL,NOME,SENHA)
