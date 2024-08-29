import duckdb
import sys

if __name__ == "__main__":
    usuario=[
        (1,"Joao","joao@gmail.com","A%sS3wnd"),
        (2,"Pedro","pedro@gmail.com","ASHSswd"),
        (3,"Ricardo","ricardo@gmail.com","#UEWH2e"),
    ]
    propriedade=[
        (1,1,"Fazenda Santa Barbara",-1111111,-999999),
        (2,2,"Instancia Laço de Ouro",-373434,436383),
        (3,3,"Fazenda Espelho D'Água",343435,-434355),
    ]
    dispositivos=[
        (1,1,"regador","51984515195151"),
        (2,2,"regador","51891981811518"),
        (3,3,"regador","19819519511117"),
    ]
    duckPath="~/"
    con=duckdb.connect(database=)