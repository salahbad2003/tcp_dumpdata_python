import csv
import webbrowser
import matplotlib.pyplot as plt
import numpy as np



#Here we will open and read our untreated file that we will treat and extract the important data from
fichier=open("C:/Users/Administrateur/Desktop/fichieràtraiter.txt", "r")

#création des listes = creating lists to fill each one with the convenable data in the tcmpdump
ipsr=[]
ipde=[]
longueur=[]
flag=[]
seq=[]
heure=[]

      # creating some counters
#compteur du nombre de flag [P] = counter for flag [P] number
flagcounterP=0
#compteur du nombre de flag [S] = counter for flag [S] number
flagcounterS=0
#compteur du nombre de flag [.] = counter for flag [.] number
flagcounter=0
#compteur des trames échangés = counter for number of frames  exchanged on network
framecounter=0
#compteur request = counter for the number of requests
requestcounter=0
#compteur reply = counter for number of replies
replycounter=0
#compteur sequence = sequences counter
seqcounter=0
#compteur acknowledgement = acknowledgments counter
ackcounter=0
#compteur window = windows counter
wincounter=0

for ligne in fichier:
    # make a split with space as delimiter
    split=ligne.split(" ")
    #delete the hexadecimal blocks and keep only the lines which contain the information
    if "IP" in ligne :
    #filling the flag list    
        framecounter+=1
        if "[P.]" in ligne :
            flag.append("[P.]")
            flagcounterP+=1
        if "[.]" in ligne :
            flag.append("[.]")
            flagcounter+=1
        if "[S]" in ligne :
            flag.append("[S]")
            flagcounterS+=1
        #filling the seq list     
        if "seq" in ligne :
            seqcounter+=1
            seq.append(split[8])
        #counting windows   
        if "win" in ligne :
            wincounter+=1
        #counting acks   
        if "ack" in ligne:
            ackcounter+=1
            
        #filling the IP source(ipsr) list  
        ipsr.append(split[2])  
        #filling the IP destination(ipde) list
        ipde.append(split[4])
        #filling the hour (heure) list
        heure.append(split[0])
        #filling the lenght (longueur) list
        if "length" in ligne:
            split = ligne.split(" ")
            if "HTTP" in ligne :
                longueur.append(split[-2])
            else: 
                longueur.append(split[-1]) 
        #to detect request and reply via ICMP protocol        
        if "ICMP" in ligne:
            if "request" in ligne:
                requestcounter+=1
            if "reply" in ligne:
                replycounter+=1

             
globalflagcounter=flagcounter+flagcounterP+flagcounterS

P=flagcounterP/globalflagcounter
S=flagcounterS/globalflagcounter
A=flagcounter/globalflagcounter 

globalreqrepcounter=replycounter+requestcounter
req=requestcounter/globalreqrepcounter
rep=replycounter/globalreqrepcounter
          
#transform all counters into lists to view them on the csv file 
flagcounter=[flagcounter]
flagcounterP=[flagcounterP]
flagcounterS=[flagcounterS]
framecounter=[framecounter]
requestcounter=[requestcounter]
replycounter=[replycounter]
seqcounter=[seqcounter]
ackcounter=[ackcounter]
wincounter=[wincounter]



# create python graphic with matplotlib library 
  #circular graphic for flags
name = ['Flag [.]', 'Flag [P]', 'Flag [S]']
data = [A,P,S]

explode=(0, 0, 0)
plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
plt.axis('equal')
plt.savefig("C:/Users/Administrateur/Desktop/graphe1.png")
plt.show()
  #circular graphic for request and reply 
name2 = ['Request' , 'Reply']
data2 = [req,rep]  
explode=(0,0)
plt.pie(data2,explode=explode,labels=name2, autopct='%1.1f%%',startangle=90, shadow=True)
plt.savefig("C:/Users/Administrateur/Desktop/graphe2.png")
plt.show()


#contenu de la page web = web page content 
htmlcontenu='''
<html>
   <head>
      <meta charset="utf-8">
      <title> Traitement des données </title>
      <style>
      body{
          background-color:#3498DB;
          }
      </style>
   </head>
   
   <body>
       <center><h2>Projet SAE 15</h2></center>
       <center><p>Sur cette page web on va vous présenter les infomations et données petinentes qu'on a trouvé dans le fichier à traiter </p></center>
       <center><h3> Nombre total des trames échangés</h3> %s</center>
       <br>
       <center><h3> Drapeaux (Flags)<h3></center>
       <center>Nombre de flags [P] (PUSH) = %s
       <br>Nombre de flags [S] (SYN) = %s  
       <br>Nombre de flag [.] (ACK) = %s
       <br>
       <br>
       <img src="C:/Users/Administrateur/Desktop/graphe1.png">
       <h3> Nombre des requests et replys </h3>
       Request = %s 
       <br>
       Reply = %s
       <br>
       <br>
       <img src="C:/Users/Administrateur/Desktop/graphe2.png">
       <h3>Statistiques entre seq et win et ack </h3>
       Nombre de seq = %s
           <br>
       Nombre de win = %s
           <br>
       Nombre de ack = %s
       
      
   </body>

</html>
'''%(framecounter,flagcounterP,flagcounterS,flagcounter,requestcounter,replycounter,seqcounter,wincounter,ackcounter)

#ouverture d'un fichier csv = open a csv file for data extracted from txt file untreated 
with open('C:/Users/Administrateur/Desktop/données.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['Heure','IP source','IP destination','Flag','Seq','Length'])
    writer.writerows(zip(heure,ipsr,ipde,flag,seq,longueur))
    fichiercsv.close()
    
#ouverture d'un fichier csv    = open a csv file for different stats
with open('C:/Users/Administrateur/Desktop/Stats.csv', 'w', newline='') as fichier2:
    writer = csv.writer(fichier2)
    writer.writerow(['Flag[P] (PUSH)','Flag[S] (SYN)','Flag[.] (ACK)','Nombre total de trames',"nombre de request","nombre de reply","nombre de sequence","nombre de acknowledg","nombre de window"])
    writer.writerows(zip(flagcounterP,flagcounterS,flagcounter,framecounter,requestcounter,replycounter,seqcounter,ackcounter,wincounter))
    fichier2.close()
    
#partie page  web = open a web page with important information and statistics
with open("C:/Users/Administrateur/Desktop/data.html","w") as html:
    html.write(htmlcontenu)
    print("page web créée avec succès")

       
fichier.close()
   
