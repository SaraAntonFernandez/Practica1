# -*- coding: utf-8 -*-

from multiprocessing import Process, Array, Value, Lock, BoundedSemaphore, Semaphore
from random import randint

NPROD = 3 # numero de productores
PROC = 8 # numero de procesos
# numero de consumidores siempre 1

def producer(pid, buffer, empty, non_empty, lock):
    k = 0
    for i in range(PROC):
        empty[pid].acquire()
        lock.acquire()
        print(f"Produciendo... {pid}")
        k += randint(0, 5)  # nuevo elemento, si los genero asi estan ya ordenados
        buffer[pid] = k
        lock.release()
        non_empty.release()
        print(f"Producido {pid}")
    buffer[pid] = -1
    print(list(buffer))
    
def consumer(buffer, empty, non_empty, lock, lst):
    while True:
        for i in range(NPROD):
            non_empty.acquire()
            
        lock.acquire()
        m = minimum(buffer)
        
        if m == -1:
            break
        
        print(f"Consumiendo...{m}")
        lst.append(buffer[m])
        lock.release()
        empty[m].release()
        print(f"Consumido {buffer[m]}")
        
        for j in range(NPROD - 1):
            non_empty.release()
        print(list(buffer))
        
def minimum(buffer):
    positives = [i for i in buffer if i>=0]
    if len(positives)==0:
        return -1
    
    lst = list(buffer)
    return lst.index(min(positives)) # posicion del minimo del buffer
    
    
def main():
    lp = [] # lista de procesos inicializada vacia
    buffer = Array('i', [0]*NPROD) # buffer compartido
    empty = [Semaphore(1)]*NPROD # lista de semaforos(1), uno por productor
    non_empty = Semaphore(NPROD) # semaforo de capacidad el numero de productores
    lock = Lock() # para el buffer
    lst = []
    
    # Productores:
    for pid in range(NPROD):
        lp.append(Process(target = producer, 
                          args=(pid, buffer, empty, non_empty, lock)))
    
    # Consumidor:
    lp.append(Process(target = consumer,
                      args=(buffer, empty, non_empty, lock, lst)))
    
    for p in lp:
        p.start()
        
    for p in lp:
        p.join()
        
if __name__=='__main__':
    main()
