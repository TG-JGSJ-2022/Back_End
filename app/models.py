import os 
def savebyjson(guardar):
    f=open("BaseDeDatos.txt","w")
    f.write(guardar)
    f.close()
    return print("Si se guardo")
    