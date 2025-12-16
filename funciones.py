import os
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#__________________________________________________________________Funciones de Cálculo__________________________________________________________________________________________


# Envío como parametro el id de un producto y me devuelve una lista con las mipymes donde se encuentra

def disponibilidad(P000):
    carpeta="data/Mipymes"
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
    



# Envío como parámetro el id de un producto y dependiendo del tipo (precio o peso) me envía la mediana de ese producto en las mypimes , si int=True me devuelve solamente el valor

def medianaP(P000,tipo,int):
    with open("E:/Economía Cuba/data/PRODUCTOS.json","r",encoding="utf-8") as f:
        Productos=json.load(f)
   
    
    Values=[]
    carpeta="data/Mipymes"
    
    #Recorro los json que se encuentran en la carpeta correspondiente para incluir a una lista el precio o peso del producto cada vez que aparece

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
   
   # Aquí hago las dos posibles variables que retorno si la longitud de la lista de valores es par o impar
   
    par=(Values[len(Values)//2]+Values[len(Values)//2-1])//2
    impar=Values[len(Values)//2] 
   
   
    if int==True:
        if len(Values)%2==0:
            return par
        else:
            return impar
        
   
   # En dependencia del tipo de valor que voy a devolver le asigno su unidad al final
  
    if tipo=="precio":
        if len(Values)%2==0:
            return f"{par} CUP"
        else:
            return f"{impar} CUP"
 
   # El producto 23 es la leche , en la cual varía su unidad de medida por lo que decido no ponerle nada al final
    if tipo=="cantidad":
        if P000=="P023":
            if len(Values)%2==0:
                return par 
            else:
                return impar
 
   # Recorro el json almacenado en una variable "Productos" para ver la unidad de medida correspondiente 
        else:
            for x in Productos:
                if x["id"]==P000:
                    peso=x["unidad"]
                    if len(Values)%2==0:
                        return f"{par} {peso}"
                    else:
                        return f"{impar} {peso}"
                
# Esta función utiliza la anterior para devolver una lista con varias medianas a la vez
            
def mediana_varios(P000,tipo,int):
    
    Medianas=[]
    
    for x in P000:
        Medianas.append(medianaP(x,tipo,int))
    
    return Medianas




# Me devuelve el valor mínimo y máximo, ya sea de los salarios estatales o del valor del dólar en un mes específico

def minmax(data,mes=None):
    with open("E:/Economía Cuba/data/El_Toque/USD_2025.json","r",encoding="utf-8") as f:
      Toque=json.load(f)
    
    with open("E:/Economía Cuba/data/Salario/Salario_Mensual_Estatal.json","r",encoding="utf-8") as f:
      Salarios=json.load(f)
    
    min=max=None
    
    if data=="salarios":
        for x in Salarios["Salarios por actividad económica"]:
            if min==None:
                min=max=Salarios["Salarios por actividad económica"][x]
        
            elif Salarios["Salarios por actividad económica"][x]<min:
                min=Salarios["Salarios por actividad económica"][x]
        
            elif Salarios["Salarios por actividad económica"][x]>max:
                max=Salarios["Salarios por actividad económica"][x]
    
    if data=="toque":
        for x in Toque[mes]:
            if min==None:
                min=max=x["valor"]
            
            elif x["valor"]<min:
                min=x["valor"]
            
            elif x["valor"]>max:
                max=x["valor"]
    
    return f"{min} CUP , {max} CUP"
            

# Lo mismo que la función anterior pero en este caso con el promedio , y en el caso de que no se especifique un mes en los parámetros devuelve una lista con todos los promedios
       
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
     
        return round(suma/cant,0)
   
    if data=="toque":
        if mes!= None:
           for x in Toque[mes]:
              suma+=x["valor"]
              cant+=1
       
           return round(suma/cant,0)
    
    # Este es el caso en que no se especifica mes  
        else:
            all=[]
            for x in Toque:
                for día in Toque[x]:
                    suma+=día["valor"]
                    cant+=1
            
                all.append(round(suma/cant,0))
                suma=0
                cant=0
          
            return all
                    
# Realiza el promedio "anual"(Enero-Noviembre) del dólar

def anualT():
    with open("E:/Economía Cuba/data/El_Toque/USD_2025.json","r",encoding="utf-8") as f:
        Toque=json.load(f)
    días=0
    cant=0
    
    for mes in Toque:
        for ds in Toque[mes]:
            días+=ds["valor"]
            cant+=1
    
    return round(días/cant,0)
            
           
                
           
    
# Convierte el salario de un sector en específico en CUP a USD tomando como referencia el Toque en el mes en el parámetro, si no se especifica hará la conversión del promedio
           
def salario_to_USD(mes,sector=None):
    with open("E:/Economía Cuba/data/Salario/Salario_Mensual_Estatal.json","r",encoding="utf-8") as f:
        Salarios=json.load(f)
    
    if sector!=None and sector!="todos":    
        conversión=round(Salarios["Salarios por actividad económica"][sector]/promed("toque",mes),0)
      
        return conversión
    
    if sector=="todos":
        conversión=[]
        
        for x in Salarios["Salarios por actividad económica"]:
            conversión.append(round(Salarios["Salarios por actividad económica"][x]/promed("toque",mes),0))

        return conversión
    else:
        conversión=round(promed("salarios")/promed("toque",mes),0)
       
        return conversión
        
    
    
# Ve la caida o ascenso del valor del dolar a largo plazo (referencia enero) o a corto plazo (referencia el mes anterior)

def porciento(mes,tipo):
    with open("E:/Economía Cuba/data/El_Toque/USD_2025.json","r",encoding="utf-8") as f:
        Toque=json.load(f)
    
    meses=[x for x in Toque] 
    prom=promed("toque")
    
    
    if tipo=="corto plazo":
        porc=round(100*prom[meses.index(mes)]/prom[meses.index(mes)-1]-100,2)
        return f"{porc}%"
    
    if tipo=="largo plazo":
        porc=round(100*prom[meses.index(mes)]/prom[0]-100,2)
        return f"{porc}%"
        
        
    










#___________________________________________________________________Graficaciones______________________________________________________________________________________________


# Evolución del valor del dólar en 2025

def grafToque():
    x=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre"]
    y=promed("toque")
    prom=anualT()
    
    plt.figure(figsize=(14,5), facecolor="#E8F5E9")  

    
    plt.gca().set_facecolor("#F1F8E9") 
    plt.plot(x, y, "o-",color="#2E7D32",linewidth=2.8,alpha=0.9,markersize=8, markerfacecolor="#66BB6A",markeredgecolor="#1B5E20")
    plt.axhline( y=prom,color="#1565C0",linestyle="--",linewidth=2.5,alpha=0.85,label=f"promedio {int(prom)} CUP")
    plt.xlabel("Meses", fontsize=14, fontweight="bold", color="#1B5E20")
    plt.ylabel("Valor del USD", fontsize=14, fontweight="bold", color="#1B5E20")
    plt.title("EL TOQUE 2025", fontsize=18,fontweight="bold",color="#0D47A1")
    plt.grid(axis="y", linestyle=":", alpha=0.5)
    plt.legend(loc="upper left",frameon=True,facecolor="white",edgecolor="black")

    return plt.show()



# Comparativa salario promedio vs costo total de productos esenciales

def grafProductos():
    Valor_Total=sum(mediana_varios(["P013","P013","P013","P013","P013","P013","P017","P020","P021","P022","P025","P025","P030","P035","P038"],"precio",int=True))
   
    
    
    
    x= "COSTO TOTAL"
    
    salario_promedio=promed("salarios")
    
    plt.figure(figsize=(14,5))
   
    plt.gca().set_facecolor("#f7f7f7")
    plt.gcf().set_facecolor("#C4C4C4")
    plt.bar(x,Valor_Total,color="#DBBF61", edgecolor="black", linewidth=1.5)
    plt.ylabel("CUP",fontsize=12,fontweight="bold")
    plt.axhline( y=salario_promedio,color="#E74C3C",linestyle="--",linewidth=2.5,alpha=0.9,label=f"Salario Promedio {int(salario_promedio)} CUP")
    plt.title("Precio productos básicos",fontsize=16,fontweight="bold",color="#333")
    plt.legend( loc="lower right", frameon=True, facecolor="white", edgecolor="gray")
    
    return plt.show()




# Salarios por actividad económica en USD

def grafSalariosUSD():
    Salarios_USD=salario_to_USD("Noviembre","todos")
    
    
    Salarios=["Transporte","Intermed Financiera","Serv Empresariales","Admin Pública","Ciencia",
              "Educación","Salud y Asist Social","Cultura y Deporte","Serv Comunales","Agricultura y Ganad","Pesca","Explotación de Minas",
              "Ind Azucarera","Ind Manufacturera","Sum Electr Gas Luz","Construcción","Comerc y Repar","Hoteles y Rest"]

    prom=salario_to_USD("Noviembre")
    
    plt.figure(figsize=(16,5))
   
    plt.gca().set_facecolor("#95e6f5")
    plt.gcf().set_facecolor("#aaadaa")
    plt.barh(Salarios,Salarios_USD,color="#034DA1", edgecolor="black", linewidth=1.5)
    plt.ylabel("Actividades Económicas",fontsize=14,fontweight="bold")
    plt.xlabel("USD",fontsize=14,fontweight="bold")
    plt.axvline(x=prom,color="#159144",linestyle="--",linewidth=2.5,alpha=0.9,label=f"Salario Promedio {int(prom)} USD")
    plt.grid(axis="x", linestyle=":", alpha=0.5)
    plt.title("Salarios Estatales por Actividad Económica en USD (tasa de cambio Noviembre)",fontsize=16,fontweight="bold",color="#333")
    plt.legend( loc="upper right", frameon=True, facecolor="white", edgecolor="gray")
    
    return plt.show()



# Gráfica interactiva para viualizar los precios medios de algunos productos , incluyendo también el peso medio .

def grafmipymes():
    with open("E:/Economía Cuba/data/PRODUCTOS.json","r",encoding="utf-8") as f:
        Productos=json.load(f)
    
    
    Productos_ids=['P001','P002','P003','P004','P005','P006','P007','P008','P009','P010',
                   'P011','P012','P013','P014','P015','P016','P017','P018','P019','P020',
                   'P021','P022','P023','P024','P025','P026','P027','P028','P029','P030',
                   'P031','P032','P033','P034','P035','P036','P038','P039','P040',
                   'P041','P042','P043']
    
    # Creo una variable que tendrá los nombres de los productos para usarlos en la gráfica
    
    Productos_name=[]
    for x in Productos_ids:
        for i in Productos:
            if x==i["id"]:
                Productos_name.append(i["nombre"])
                

    precios=mediana_varios(Productos_ids,"precio",int=True)
    precios_str=mediana_varios(Productos_ids,"precio",int=False)
    pesos_str=mediana_varios(Productos_ids,"cantidad",int=False)   
     
    # Aquí la lista de pesos que están en string separo el valor int del tipo de unidad de medidad del producto
    
    pesos=[]
    unidades=[]
    
    for p in pesos_str:
        if p==None:
            pesos.append(None)
            unidades.append(None)
        elif type(p)==int:
            pesos.append(p)
            unidades.append("variable")
        else:
            valor,unidad=p.split()
            pesos.append(int(valor))
            unidades.append(unidad)
    
    hover_text=[
        f"<b>Producto:</b> {pid}<br><b>Precio:</b> {pr}<br><b>Peso:</b> {pw}<br><b>Unidad:</b> {un}"
        for pid,pr,pw,un in zip(Productos_name,precios_str,pesos,unidades)
    ]

    # Preparo las variables que utilizaré en dos categorías , productos que posean unidad de medida y productos que no poseen 

    x_con_peso=[]
    y_con_peso=[]
    text_con_peso=[]
    color_con_peso=[]
    simbolo_con_peso=[]
    size_con_peso=[]

    x_sin_peso=[]
    y_sin_peso=[]
    text_sin_peso=[]
    size_sin_peso=[]

    for x,y,u,t,p in zip(pesos,precios,unidades,hover_text,precios):
        if x is None:
            x_sin_peso.append(-50)
            y_sin_peso.append(y)
            text_sin_peso.append(t)
            size_sin_peso.append(max(8,min(p/200,30)))
        else:
            x_con_peso.append(x)
            y_con_peso.append(y)
            text_con_peso.append(t)
            size_con_peso.append(max(8,min(p/200,30)))
            if u=="gr":
                color_con_peso.append("#4C78A8")
                simbolo_con_peso.append("circle")
            elif u=="ml":
                color_con_peso.append("#F58518")
                simbolo_con_peso.append("diamond")
            elif u=="variable":
                color_con_peso.append("#54A24B")
                simbolo_con_peso.append("square")
            else:
                color_con_peso.append("#B0B0B0")
                simbolo_con_peso.append("circle")

    # Con las variables listas realizo el proceso de graficaciön

    Fig=go.Figure()

    Fig.add_trace(go.Scatter(
        x=x_con_peso,y=y_con_peso,mode="markers",
        text=text_con_peso,hoverinfo="text",
        marker=dict(size=size_con_peso,color=color_con_peso,symbol=simbolo_con_peso,
                    opacity=0.8,line=dict(width=1.5,color="white")),
        name="Con peso"
    ))

    Fig.add_trace(go.Scatter(
        x=x_sin_peso,y=y_sin_peso,mode="markers",
        text=text_sin_peso,hoverinfo="text",
        marker=dict(size=size_sin_peso,color="#B0B0B0",symbol="x",
                    opacity=0.9,line=dict(width=2,color="black")),
        name="Sin peso"
    ))

    Fig.update_layout(
        title=dict(text="Precio medio vs Peso medio por producto",x=0.5,font=dict(size=20)),
        xaxis=dict(title="Peso / Volumen",showgrid=True,gridcolor="rgba(200,200,200,0.4)",
                   zeroline=False),
        yaxis=dict(title="Precio medio (CUP)",showgrid=True,gridcolor="rgba(200,200,200,0.4)",
                   zeroline=False),
        plot_bgcolor="white",paper_bgcolor="white",
        hovermode="closest",
        margin=dict(l=60,r=40,t=80,b=60)
    )
    
    return Fig.show()



