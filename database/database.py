import duckdb
import sys
import os


#Cria a tabela com os dados dos usuarios.
def table_usuario(duckPath):
  con=duckdb.connect(database=duckPath, read_only=False)
  con.sql(f"CREATE TABLE USUARIO(ID INT PRIMARY KEY,EMAIL VARCHAR,NOME VARCHAR,SENHA VARCHAR)")
  con.close()


#Cria a tabela com os dados das propriedades. Cada usuario poderá ter N propriedades.
def table_propriedade(duckPath):
  con=duckdb.connect(database=duckPath, read_only=False)
  con.sql(f"CREATE TABLE PROPRIEDADE(ID INT PRIMARY KEY,ID_USUARIO INT,NOME VARCHAR,LATITUDE FLOAT,LONGITUDE FLOAT,FOREIGN KEY(ID_USUARIO) REFERENCES USUARIO(ID))")
  con.close()


#Cria a tabela com os dados dos dispositivos de irrigação. Cada propriedade poderá ter N dispositivos.
def table_dispositivo(duckPath):
  con=duckdb.connect(database=duckPath, read_only=False)
  con.sql(f"CREATE TABLE DISPOSITIVO(ID INT PRIMARY KEY,ID_PROPRIEDADE INT,NOME VARCHAR,CODIGO VARCHAR,FOREIGN KEY(ID_PROPRIEDADE) REFERENCES PROPRIEDADE(ID))")
  con.close()


def destruir_tables(duckPath):
  con=duckdb.connect(database=duckPath,read_only=False)
  con.sql("DROP TABLE IF EXISTS DISPOSITIVO")
  con.sql("DROP TABLE IF EXISTS PROPRIEDADE")
  con.sql("DROP TABLE IF EXISTS USUARIO")
  con.close()


def novo_cadastro(duckPath,EMAIL,NOME,SENHA):
  con=duckdb.connect(database=duckPath, read_only=False)
  con.sql(f"INSERT INTO CADASTRO(EMAIL,NOME,SENHA) VALUES ('{EMAIL}','{NOME}','{SENHA}')")
  con.close()


def excluir_cadastro(duckPath,EMAIL):
   con=duckdb.connect(database=duckPath, read_only=False)
   con.sql(f"DELETE FROM CADASTRO WHERE EMAIL='{EMAIL}'")


if __name__ == "__main__":
  #EMAIL = sys.argv[1]
  #NOME = sys.argv[2]
  #SENHA = sys.argv[3]
  duckPath='~/Hydro-Cultiva-Connect/database/database'
  destruir_tables(duckPath)
  table_usuario(duckPath)
  table_propriedade(duckPath)
  table_dispositivo(duckPath)


