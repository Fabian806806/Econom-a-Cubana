import os
import json

with open("E:/Economía Cuba/data/PRODUCTOS.json","r",encoding="utf-8") as f:
    Productos=json.load(f)

with open("E:/Economía Cuba/data/El_Toque/USD_2025.json","r",encoding="utf-8") as f:
    Toque=json.load(f)
    
with open("E:/Economía Cuba/data/Salario/Salario_Mensual_Estatal.json","r",encoding="utf-8") as f:
    Salarios=json.load(f)



def disponibilidad(P000):
    carpeta="data/Mypimes"
    mypimes=[]
    
    for archivo in os.listdir(carpeta):
        ruta=os.path.join(carpeta,archivo)
     
        with open(ruta,"r",encoding="utf-8") as f:
            data=json.load(f)
            
        for x in data["productos"]:
            if x["id_producto"]==P000:
                mypimes.append(data["id"])
                break
        
    return mypimes
    





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






def maxmin(data,mes=None):
    with open("E:/Economía Cuba/data/El_Toque/USD_2025.json","r",encoding="utf-8") as f:
      Toque=json.load(f)
    
    with open("E:/Economía Cuba/data/Salario/Salario_Mensual_Estatal.json","r",encoding="utf-8") as f:
      Salarios=json.load(f)
    
    min=max=None
    
    if data=="salarios":
        for x in Salarios["Salarios por actividad económica"]:
            if min==None:
                min=max=data["Salarios por actividad económica"][x]
        
            elif data["Salarios por actividad económica"][x]<min:
                min=data["Salarios por actividad económica"][x]
        
            elif data["Salarios por actividad económica"][x]>max:
                max=data["Salarios por actividad económica"][x]
    
    if data=="toque":
        for x in Toque[mes]:
            if min==None:
                min=max=x["valor"]
            
            elif x["valor"]<min:
                min=x["valor"]
            
            elif x["valor"]>max:
                max=x["valor"]
    
    return f"{min} CUP , {max} CUP"
            
       
def promed(data,mes=None):
    with open("E:/Economía Cuba/data/El_Toque/USD_2025.json","r",encoding="utf-8") as f:
         Toque=json.load(f)
    
    with open("E:/Economía Cuba/data/Salario/Salario_Mensual_Estatal.json","r",encoding="utf-8") as f:
         Salarios=json.load(f)
   
    suma=0
    cant=0
    
    if data=="salarios":
        for x in Salarios["Salarios por actividad económica"]:
            suma+=Salarios["Salarios por actividad económica"][x]
            cant+=1
     
        return round(suma/cant,1)
   
    if data=="toque":
        if mes!= None:
           for x in Toque[mes]:
              suma+=x["valor"]
              cant+=1
       
           return round(suma/cant,1)
      
        else:
            all=[]
            for x in Toque:
                for día in Toque[x]:
                    suma+=día["valor"]
                    cant+=1
            
                all.append(round(suma/cant,1))
                suma=0
                cant=0
          
            return all
                    
            
           
    
  


           









def salario_to_USD(sector):
    conversión=round(Salarios["Salarios por actividad económica"][sector]/promed(Toque),1)
    
    return f"{conversión} USD"


      