import os 
def savebyjson(guardar):
    
    f=open("BaseDeDatos.txt","a")
    f.write(str(guardar))
    f.close()
    return print("Si se guardo")
    