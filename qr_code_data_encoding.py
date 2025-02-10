
def transformare(sir_citire, error_level, strucuted_append, position, length, parity):
    carnat_final = "" if not strucuted_append else f"0011{format(position, '04b')}{format(length,'04b')}{format(parity, "08b")}"
    carnat_final+="0100" # initializam cu modul folosit adica byte
    lungime_sir_citire=len(sir_citire)
    # determinam versiunea in care ne incadram
    indice=0
    from qr_code_character_capacities import dict

    for i in range (0,len(dict[error_level])):
        if(dict[error_level][i][1]>=lungime_sir_citire + 4):
            indice=i
            break

    versiune=dict[error_level][indice][0]
    lgdorita=len(bin(lungime_sir_citire)[2:])
    if(versiune<=9):
        lgdorita=8-lgdorita
    else:
        lgdorita=16-lgdorita
    # adaugam zerouri pentru a avea lungimea sirului in biti dorita

    adaugare=""
    while(lgdorita!=0):
        adaugare=adaugare+"0"
        lgdorita-=1
    adaugare=adaugare+str(bin(len(sir_citire)))[2:]
    carnat_final=carnat_final+adaugare
    adaugare=""
    for x in sir_citire:
        ch=bin(ord(x))[2:]
        lungime_adaugare=8-len(ch)
        sir_nou=""
        while(lungime_adaugare!=0):
            sir_nou=sir_nou+"0"
            lungime_adaugare-=1
        for lit in ch:
            sir_nou=sir_nou+lit
        # print(sir_nou,chr(int(sir_nou,2)))
        adaugare=adaugare+sir_nou
    carnat_final=carnat_final+adaugare
    lungime=len(carnat_final)
    from qr_code_total_codewords import dict_total
    lgdorita=dict_total[(error_level,versiune)][0]*8
    lgdorita=lgdorita-lungime
    adaugare=""
    if(lgdorita<=4):
        chestie=lgdorita
        while(chestie!=0):
            adaugare=adaugare+"0"
            chestie-=1
    else:
        chestie=4
        while(chestie!=0):
            adaugare=adaugare+"0"
            chestie-=1
    carnat_final=carnat_final+adaugare
    lungime=len(carnat_final)
    while(lungime%8!=0):
        carnat_final=carnat_final+"0"
        lungime=len(carnat_final)
    # codul lui 236 este 11101100
    # codul lui 17  este 00010001
    lgdorita=dict_total[(error_level,versiune)][0]*8
    alternativ=0
    while(lungime<lgdorita):
        if(alternativ==0):
            carnat_final=carnat_final+"11101100"
        else:
            carnat_final=carnat_final+"00010001"
        alternativ=(alternativ+1)%2
        lungime=len(carnat_final)
    lista=[]
    # carnat_final=carnat_final[4:]
    lungime=len(carnat_final)

    for i in range(0,lungime,8):
        block=carnat_final[i:(i+8)]
        lista.append(block)
    nrbloc1=dict_total[(error_level,versiune)][1]
    nrword1=dict_total[(error_level,versiune)][2]
    nrbloc2=dict_total[(error_level,versiune)][3]
    nrword2=dict_total[(error_level,versiune)][4]
    ind=-1
    lista_finala=[]
    while(nrbloc1!=0):
        adaugare_bloc=[]
        aux=nrword1
        while(aux!=0):
            ind=ind+1
            adaugare_bloc.append(int(lista[ind], 2))
            aux-=1
        lista_finala.append(adaugare_bloc)
        nrbloc1-=1
    while(nrbloc2!=0):
        adaugare_bloc=[]
        aux=nrword2
        while(aux!=0):
            ind=ind+1
            adaugare_bloc.append(int (lista[ind], 2))
            aux-=1
        nrbloc2-=1
        lista_finala.append(adaugare_bloc)
    return lista_finala, versiune


