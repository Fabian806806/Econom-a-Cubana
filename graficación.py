import json 
import matplotlib.pyplot as plt
import funciones as mf


def grafToque():
   
   
    x=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre"]
    y=mf.promed("toque")
    
    plt.figure(figsize=(14,5) , facecolor="green")
    plt.plot(x , y ,"o-", color="green" , linewidth=2.4 , alpha=0.95)
    plt.xlabel("Meses")
    plt.ylabel("Valor del USD")
    plt.title("EL TOQUE 2025")
    
    
    return plt.show()


print(grafToque())