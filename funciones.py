import os
import json

with open("E:/Economía Cuba/data/PRODUCTOS.json","r",encoding="utf-8") as f:
    Productos=json.load(f)

with open("E:/Economía Cuba/data/El_Toque/USD_Noviembre.json",encoding="utf-8") as f:
    Toque=json.load(f)


def medianaP(P000,tipo="precio"):
    global Productos
    
    Values=[]
    carpeta="data/Mypimes"

    for archivo in os.listdir(carpeta):
        ruta=os.path.join(carpeta,archivo)
     
        with open(ruta,"r",encoding="utf-8") as f:
            data=json.load(f)
         
        for x in data["productos"]:
            if x["id_producto"]==P000 and x["especificaciones"][tipo]!=None:
                Values.append(x["especificaciones"][tipo])
    
    if Values==[]:
        return None
   
    Values.sort()
    par=(Values[len(Values)//2]+Values[len(Values)//2+1])//2
    impar=Values[len(Values)//2] 
    
    if tipo=="precio":
        if len(Values)%2==0:
            return f"{par} CUP"
        else:
            return f"{impar} CUP"
   
    if tipo=="cantidad":
        if P000=="P023":
            if len(Values)%2==0:
                return par 
            else:
                return impar
        else:
            for x in Productos:
                if x["id"]==P000:
                    peso=x["unidad"]
                    if len(Values)%2==0:
                        return f"{par} {peso}"
                    else:
                        return f"{impar} {peso}"
                
            
def mediana_varios(MP000,tipo="precio"):
    
    Medianas=[]
    
    for x in MP000:
        Medianas.append(medianaP(x,tipo))
    
    return Medianas


            



        