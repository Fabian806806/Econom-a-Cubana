import os
import json

carpeta="data/Mypimes"

for archivo in os.listdir(carpeta):
    ruta=os.path.join(carpeta,archivo)
    
    with open(ruta,"r",encoding="utf-8") as f:
       data=json.load(f)
    
    for producto in data["productos"]:
         for key in producto["especificaciones"]:
              if producto["especificaciones"][key]==350:
                  producto["especificaciones"][key]=355
            
        
       
        
       
            
    with open(ruta,"w",encoding="utf-8") as f:
         json.dump(data,f,indent=2,ensure_ascii=False)