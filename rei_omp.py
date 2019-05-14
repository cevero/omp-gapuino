#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#o script a seguir deve ler e traduzir um codigo em openmp para mbedos
#include "gap_cluster.h"
import sys
import re
title=sys.argv[1]
#teste

arq1=open(str(title),'r')

title2 = title.split(".c")[0]
arq2=open("output/"+str(title2)+"_gap.c",'w')

arq2.write("#include "+"\"cmsis.h\"\n")
arq2.write("#include "+ "\"gap_common.h\"\n")
arq2.write("#include "+"\"mbed_wait_api.h\"\n")

arq2.write("// FEATURE_CLUSTER\n")
arq2.write("#include "+"\"gap_cluster.h\"\n")
arq2.write("#include "+"\"gap_dmamchan.h\"\n")
arq2.write("#include "+"<time.h>\n")
arq2.write("#include <stdlib.h>\n")
arq2.write("#define CORE_NUMBER   (8)\n")



#def hascbrackets():
#    if flagchave2 == 0:
#        return 1
#    elif re.search("{",linha):#tem chaves internas
#        
#                flagchave2=flagchave2+linha.count("{")-linha.count("}")
#    elif re.search("}",linha):
#                flagchave2=flagchave2-linha.count("}")
#

flagchave2 = 0
flagchave = 0
flagomp = 0
func = []
functions=[]
texto = []
contador = 0
flagpf = 0
#it = iter(arq1)
library =[]
structures =[]
count_parallelfor=0
it_arq1 = iter(arq1)
lista_var_pf=[]
schedule = 1
prov_vars_private = ""
prov_vars_shared = ""
red_oper=""
red_var=""
flag_red=0



##############################################################################
#               _       __              _ _ _                    _           #
# ___  ___  ___| | __  / _| ___  _ __  | (_) |__  _ __ __ _ _ __(_) ___  ___ #
#/ __|/ _ \/ _ \ |/ / | |_ / _ \| '__| | | | '_ \| '__/ _` | '__| |/ _ \/ __|#
#\__ \  __/  __/   <  |  _| (_) | |    | | | |_) | | | (_| | |  | |  __/\__ \#
#|___/\___|\___|_|\_\ |_|  \___/|_|    |_|_|_.__/|_|  \__,_|_|  |_|\___||___/#
#                                                                            #
##############################################################################
for linha in arq1:
    linha=linha.rstrip()
    if re.search("<stdio>", linha):
        continue
    elif re.search("omp.h", linha):
        continue
    elif re.search("include",linha) or re.search("define",linha):
        library.append(linha)
        continue
#######################################################################
#                           _       __                                # 
#             ___  ___  ___| | __  / _| ___  _ __                     #
#            / __|/ _ \/ _ \ |/ / | |_ / _ \| '__|                    #
#            \__ \  __/  __/   <  |  _| (_) | |                       #
#            |___/\___|\___|_|\_\ |_|  \___/|_|                       #
#                                                                     #
#                                                                     #
#                                                                     #
#                                                                     #
#                             _ _      _                              #
#       _ __   __ _ _ __ __ _| | | ___| |  _______  _ __   ___  ___   #
#      | '_ \ / _` | '__/ _` | | |/ _ \ | |_  / _ \| '_ \ / _ \/ __|  #
#      | |_) | (_| | | | (_| | | |  __/ |  / / (_) | | | |  __/\__ \  #
#      | .__/ \__,_|_|  \__,_|_|_|\___|_| /___\___/|_| |_|\___||___/  #
#      |_|                                                            #
#                                                                     #
#                                                                     #
#                                                                     #
#                                                                     #
#######################################################################


    if re.search("pragma",linha) and re.search("omp",linha)and re.search("parallel",linha) and (not re.search("for",linha)): #é regiao paralela?

        flagomp = 1
        texto.append("parallel_function"+str(contador)+"(0)\n")
        continue




    elif re.search("pragma",linha) and re.search("omp",linha) and re.search("parallel",linha) and re.search("for",linha):       
    
        
        
        if not re.search("default",linha):
                print(linha)
                print("use default(none) specifying public and shared variables directive to parallel for")
                break;
        else:
                prov_struct = []
               ##############################################################
        #######verivy if have a reduction clause and identify the variable #########
               #############################################################
                if re.search("reduction",linha) or re.search("reduction\(",linha):
                    reduct = re.findall(r'reduction\((.+)\)',linha)[0].split(":")
                    red_oper = reduct[0]
                    red_var = reduct[1]
                    texto.append("estrutura"+str(count_parallelfor)+'->'+red_var+"="+red_var+";\n")
                    flag_red = 1
                prov_vars_private = re.findall(r'private\((.*?)\)',linha)[0].split(',')
                prov_vars_shared = re.findall(r'shared\((.*?)\)',linha)[0].split(',')
                if flag_red:
                    prov_vars_shared.append(red_var)
                prov_vars = prov_vars_shared+prov_vars_private
                var_len = len(prov_vars_shared)+ len(prov_vars_private) 
                for vari in range(var_len):
                    prov_struct.append("int "+str(prov_vars[vari])+";\n")
                    lista_var_pf.append(vari)
                    texto.append("estrutura"+str(count_parallelfor)+"->"+str(prov_vars[vari])+"="+str(prov_vars[vari])+";\n")
                structures.append(prov_struct)
                texto.append("CLUSTER_Start(0, CORE_NUMBER);\n")
                texto.append("estrutura"+str(count_parallelfor)+"=malloc(CORE_NUMBER*sizeof(L1_structure"+str(count_parallelfor)+"));\n");
                flagpf=1
                continue

#############################################################
#                                               _ _      _  #
#  ___  _ __ ___  _ __    _ __   __ _ _ __ __ _| | | ___| | #
# / _ \| '_ ` _ \| '_ \  | '_ \ / _` | '__/ _` | | |/ _ \ | #
#| (_) | | | | | | |_) | | |_) | (_| | | | (_| | | |  __/ | #
# \___/|_| |_| |_| .__/  | .__/ \__,_|_|  \__,_|_|_|\___|_| #
#                |_|     |_|                                #
#############################################################


    if flagomp: #to dentro de um pragma?
        if re.search("pragma",linha) and re.search("omp",linha) and re.search("single",linha):
            func.append("if(omp_get_thread_num()==0)\n")
            continue
        if(re.search("{",linha)and flagchave == 0):
            flagchave = 1
        elif not flagchave:#a zona paralela é só a próxima linha
            flagomp = 0
            contador = contador +1
            func.append("\n"+linha)
            functions.append(func)
            func = []
        elif flagchave:#estamos dentro de uma zona paralela
                func.append(linha+"\n")
                if re.search("{",linha):#tem chaves internas
                        flagchave2=flagchave2+linha.count("{")-linha.count("}")
                elif re.search("}",linha):
                        flagchave2=flagchave2-linha.count("}")
                elif(flagchave2==0 and re.search("}",linha)):
                        flagchave=0
                        flagomp = 0
                        contador = contador +1
                        functions.append(func)
                        func = []

##############################################################################
#                                               _ _      _    __             #
#  ___  _ __ ___  _ __    _ __   __ _ _ __ __ _| | | ___| |  / _| ___  _ __  #
# / _ \| '_ ` _ \| '_ \  | '_ \ / _` | '__/ _` | | |/ _ \ | | |_ / _ \| '__| #
#| (_) | | | | | | |_) | | |_) | (_| | | | (_| | | |  __/ | |  _| (_) | |    #
# \___/|_| |_| |_| .__/  | .__/ \__,_|_|  \__,_|_|_|\___|_| |_|  \___/|_|    #
#                |_|     |_|                                                 #
#                                                                            # 
##############################################################################

    elif flagpf==1:



        #lets seek for iterator var and limmit of iteration
        for_iter = re.findall("(\(.*\;)",linha)[0]
        for_stop = re.findall("\;.*\;",linha)[0]
        for_modifier = re.findall("(\;[^\;)]*\))",linha)[0]

        if re.search(">=",for_stop):
            n = for_stop.split(">=")[1]
            i = for_stop.split(">=")[0]
            operator = ">="
        elif re.search("<=",for_stop):
            n = for_stop.split("<=")[1]
            i = for_stop.split("<=")[0]
            operator = "<="
        elif re.search("!=",for_stop):
            n = for_stop.split("!=")[1]
            i = for_stop.split("!=")[0]
            operator = "!="
        elif re.search("<",for_stop):
            n = for_stop.split("<")[1]
            i = for_stop.split("<")[0]
            operator = "<"
        elif re.search(">",for_stop):
            n = for_stop.split(">")[1]
            i = for_stop.split(">")[0]
            operator = ">"
        n = n.split(";")[0].strip()
        if n.isdigit():
            texto.append("new_n = "+n+"\n")

        i = i.split(";")[1].strip()
        modifier = for_modifier.split(";")[1].split(")")[0].strip()
        starter = for_iter.split("=")[1].split(";")[0].strip()
            #########################################
       ######appending the new for function parallel#########
            #########################################
        func.append("L1_structure"+str(count_parallelfor)+"* L1_structure = malloc(sizeof(L1_structure"+str(count_parallelfor)+"));\n")
        func.append("L1_structure = estrutura"+str(count_parallelfor)+";\n")
        func.append("int new_n = (L1_structure->"+str(n)+"/CORE_NUMBER)*(omp_get_thread_num()+1);\n")
        if re.search("int",for_iter):
            #texto.append("int "+i+";\n" )
            func.append("for(int "+i+"= "+str(starter)+"+(L1_structure->"+str(n)+"/CORE_NUMBER)*omp_get_thread_num(); "+i+operator+"new_n;"+modifier+")\n{\n")
        else:
            func.append("for(L1_structure"+str(count_parallelfor)+"->"+i+"="+str(starter)+"+ (L1_structure->"+str(n)+"/CORE_NUMBER)*omp_get_thread_num(); L1_structure"+str(count_parallelfor)+"->"+i+operator+"new_n;"+modifier+")\n{\n")
        ##texto.append("estrutura"+str(count_parallelfor)+"->"+i+"= "+i+";\n")
        texto.append("estrutura"+str(count_parallelfor)+"->"+str(n)+" = "+str(n)+";\n")
        texto.append("\nparallelfor_function"+str(count_parallelfor)+"(0)\n")
#need no more append the for limmits
        structures[count_parallelfor].append("int "+str(n)+";\n")
       # structures[count_parallelfor].append("int "+str(i)+";\n")
        flagpf=2




    elif flagpf==2:

        if re.search("pragma",linha)and re.search("omp",linha) and re.search("single",linha):
            func.append("if(omp_get_thread_num()==0)\n")
            continue
        if(re.search("{",linha)and flagchave == 0):
            flagchave = 1
        elif not flagchave:#o for é só a próxima linha
            #replacing shared variables with actual structure
            flagpf = 0
            contador = contador +1
            func.append("\n"+linha+"\n")
            func.append("\n}\n")
            functions.append(func)
            func = []




        elif flagchave:#estamos dentro de um for paralelo
                
                
                func.append("\n"+linha+"\n")
            
                
                
                if(flagchave2==0 and re.search("}",linha)):

                        flagchave=0
                        flagpf = 0
                        contador = contador +1
                        print(prov_vars_shared)
                        rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                        rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))
                        func2=[]
                        
                        
                        
                        for prov_line in func:
                            if re.search("\"",prov_line):
                                prov2_line = prov_line.split("\"")
                                prov3_line = ''.join(rp.sub(r"L1_structure->\1",prov_line)).split("\"")
                                func2.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                continue
                            func2.append(''.join(rp.sub(r"L1_structure->\1",prov_line)))
                        func3=[]
                        
                        
                        
                        
                        for prov_line in func2:
                            structu="estrutura"+str(count_parallelfor)+"->"
                            if re.search("\"",prov_line):
                                prov2_line = prov_line.split("\"")
                                prov3_line = ''.join(rs.sub("estrutura"+str(count_parallelfor)+'->'+r'\1',prov_line)).split("\"")
                                func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                continue
                            func3.append(''.join(rs.sub("estrutura"+str(count_parallelfor)+'->'+r'\1',prov_line)))
                        
                        
                        
                        
                        
                        
                        
                        
                        if flag_red:
                            func3.append("EU_MutexLock(0);\n")
                            func3.append("\nestrutura"+str(count_parallelfor)+"->"+red_var+"=estrutura"+str(count_parallelfor)+"->"+red_var+red_oper+"L1_structure->"+red_var+";\n")
                            func3.append("EU_MutexUnlock(0);\n")
                            texto.append(red_var+"=estrutura"+str(count_parallelfor)+"->"+red_var+";\n")
                        functions.append(func3)
                        func = []
                        func2 = []
                        prov_vars_shared = []
                        prov_vars_private = []
                        prov_vars = []
                        count_parallelfor = count_parallelfor+1
                elif re.search("{",linha):#tem chaves internas
                        flagchave2=flagchave2+linha.count("{")-linha.count("}")
                elif re.search("}",linha):
                        flagchave2=flagchave2-linha.count("}")






    else:#nao e regiao paralela
         texto.append(linha)
#lets define the generic functions to be called



#####################################
#               _ _   _             #  
#__      ___ __(_) |_(_)_ __   __ _ # 
#\ \ /\ / / '__| | __| | '_ \ / _` |# 
# \ V  V /| |  | | |_| | | | | (_| |# 
#  \_/\_/ |_|  |_|\__|_|_| |_|\__, |#  
#                             |___/ #  
#                                   #  
# _ __   _____      __              #    
#| '_ \ / _ \ \ /\ / /              #
#| | | |  __/\ V  V /               #  
#|_| |_|\___| \_/\_/                #    
#                                   #   
#                _     _            # 
#  __ _ _ __ ___| |__ (_)_   _____  # 
# / _` | '__/ __| '_ \| \ \ / / _ \ # 
#| (_| | | | (__| | | | |\ V /  __/ # 
# \__,_|_|  \___|_| |_|_| \_/ \___| # 
#                                   # 
#####################################




for linha in library:
    arq2.write(linha+"\n")
len_structures = len(structures)
print(str(len_structures)+" é a quantidade de estruturas")
print(structures)
for cont2 in range(len_structures):
    arq2.write("typedef struct L1_structure"+str(cont2)+"{\n")
    #structures[cont2].append("int IDstructure;\n")
    arq2.writelines(structures[cont2])
    arq2.write("}L1_structure"+str(cont2)+";\n")
    arq2.write("L1_structure"+str(cont2)+"* estrutura"+str(cont2)+";\n")
    #arq2.write("estrutura"+str(cont2)+"->IDstructure="+str(cont2)+";\n")
######################################################
#lembre de alocar os structs e de liberar depois
for cont2 in range (contador):#escreve as funcoes das zonas paralelas
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+"){\n")
    arq2.writelines(functions[cont2])
    arq2.write("\n}\n")

arq2.write("void caller(void* arg){\n")
arq2.write("int x = (int)arg;\n")
for cont2 in range (contador):
        arq2.write("if(x =="+str(cont2)+")return generic_function"+str(cont2)+"(x);\n")
arq2.write("}\n")
arq2.write("\n\n")
arq2.write("void Master_Entry(void *arg) {\n")
arq2.write("    CLUSTER_CoresFork(caller, arg);\n")
arq2.write("}\n")

count2pf = count_parallelfor
cont_paral = contador
for linha in texto:
    #ligando e desligando o cluster
    if re.search("parallel_function",linha):
        arq2.write("CLUSTER_Start(0, CORE_NUMBER);\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador- cont_paral)+", 0);\n")
        cont_paral = cont_paral - 1
        arq2.write("CLUSTER_Wait(0);\n")
        arq2.write("CLUSTER_Stop(0);\n")
    elif re.search("parallelfor_function",linha):
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador- cont_paral)+", 0);\n")
        arq2.write("CLUSTER_Wait(0);\n")
        for vari in
        arq2.write("free(estrutura"+str(count_parallelfor-count2pf)+");\n");
        cont_paral = cont_paral - 1
        count2pf = count2pf-1
        arq2.write("CLUSTER_Stop(0);\n")

    else:
         arq2.write(linha+"\n")# o fim do arquivo chegou
arq1.close()
arq2.close()

