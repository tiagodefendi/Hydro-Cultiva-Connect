import duckdb
import sys

if __name__ == "__main__":
    duckPath = '~/Hydro-Cultiva-Connect/database/database'
    usuarios=[
      #  (1,"Joao","joao@gmail.com","A3sS3wnd"),
       # (2,"Pedro","pedro@gmail.com","ASHSswd"),
        #(3,"Ricardo","ricardo@gmail.com","#UEWH2e"),
    ]
    propriedades=[
     #   (1,1,"Fazenda Santa Barbara",-1111111,-999999),
      #  (2,2,"Instancia Laço de Ouro",-373434,436383),
        (3,3,"Fazenda Espelho Dagua",343435,-434355),
    ]
    dispositivos=[
     #   (1,1,"regador","51984515195151"),
      #  (2,2,"regador","51891981811518"),
        (3,3,"regador","19819519511117"),
    ]
    
    con=duckdb.connect(database=duckPath, read_only=False)

    for usuario in usuarios:
        con.sql(f"INSERT INTO USUARIO (ID,EMAIL,NOME,SENHA) VALUES ({usuario[0]},'{usuario[1]}','{usuario[2]}','{usuario[3]}')")

    for propriedade in propriedades:
        con.sql(f"INSERT INTO PROPRIEDADE (ID,ID_USUARIO,NOME,LATITUDE,LONGITUDE) VALUES ({propriedade[0]},{propriedade[1]},'{propriedade[2]}','{propriedade[3]}','{propriedade[4]}')")

    for dispositivo in dispositivos:
        con.sql(f"INSERT INTO DISPOSITIVO (ID,ID_PROPRIEDADE,NOME,CODIGO) VALUES ({dispositivo[0]},{dispositivo[1]},'{dispositivo[2]}','{dispositivo[3]}')")

    con.close()
