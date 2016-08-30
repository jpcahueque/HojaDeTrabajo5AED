# Universidad del Valle de Guatemala
#Jorge Tezen 15417
#Juan Pablo Cahueque 15
# Este codigo esta basado en ejemplos anteriores y de ejemplos en clase

import simpy
import random
import math
vel = 3  #puede variar la velociad del procesador 
memoria_ram= 100 #puede variar la cantidad de memoria 
numProcesos = 50   #el numero de procesos puede variar 
tiempoT=0.0
tiempos=[] 


def proceso(env, tprocesos, nom, ram, ram_util, numInst, vel):

    global tiempoT
    global tiempos

    #New El proceso llega al sistema operativo espera a que se le asigne RAM
    yield env.timeout(tprocesos)
    print('%s solicita %d de RAM (new)' % ( nom, ram_util))
    tgeneracion = env.now  #tiempo que tarda en generarse el proceso
    
    #Ready solicita RAM
    yield ram.get(ram_util)
    print('%s. Solicitud aceptada por %d de RAM (admitted)' % ( nom, ram_util))
    insComp = 0
    
    while insComp < numInst:

        #conexion CPU
        with cpu.request() as req:
            yield req
            #instruccion a realizarse
            if (numInst-insComp)>=vel:
                inst_exe=vel
            else:
                inst_exe=(numInst-insComp)

            print('%s se ejecutara. El CPU ejecutara %d instrucciones. (ready)' % (nom, inst_exe))
            #tiempo de instrucciones a ejecutar
            yield env.timeout(inst_exe/vel)   

            #numero total de intrucciones terminadas
            insComp += inst_exe
            print('%s se esta procesando (%d/%d) completado. (running)' % ( nom, insComp, numInst))

        #Si la decision es 1 wait, si es 2 procedemos a ready
        desicion = random.randint(1,2)

        if desicion == 1 and insComp<numInst:
            #(waiting)
            with wait.request() as req2:
                yield req2
                yield env.timeout(1)                
                print('%s. Concluyeron operaciones I/O. (waiting)' % ( nom))
   
    #Cantidad de RAM
    yield ram.put(ram_util)
    print('%s consumio %d de RAM. (terminated)' % (nom, ram_util))
    tiempoT += (env.now - tgeneracion)
    #se guarda tiemposo
    tiempos.append(env.now - tgeneracion) 


#recursos en simulacion    
env = simpy.Environment() 
cpu = simpy.Resource (env, capacity=2) #Cola de tipo Resource para el CPU, con la cantidad de procesadores variable 
ram = simpy.Container(env, init=memoria_ram, capacity=memoria_ram) #Cola de tipo Container para la RAM
wait = simpy.Resource (env, capacity=2) #Wait para operaciones I/O

#Semilla del random
interval = 10 #numero de intervalos (que va variando)
random.seed(8976)


#Ejecucion de la Simulacion
for i in range(numProcesos):
    tprocesos = random.expovariate(1.0 / interval)
    numInst = random.randint(1,10)
    ram_util = random.randint(1,10) #Se genera una cantidad aleatoria de memoria
    env.process(proceso(env, tprocesos, 'Proceso %d' % i, ram, ram_util, numInst, vel))

#Se corre la simulacion
env.run()

#tiempo promedio de los procesos
print " "
print ('El tiempo total de ejecucion es %f segundos' %(tiempoT))
prom=(tiempoT/numProcesos)
print('El tiempo promedio de los procesos es: %f segundos \n' % (prom))


#calculo desviacion estandar
sumatoria=0

for cont in tiempos:
    sumatoria+=(cont-prom)**2

desv= math.sqrt(sumatoria/(numProcesos-1))
print ('La desviacion estandar de los tiempos de los procesos ejecutados es: %f segundos' %(desv))


