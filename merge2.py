# -*- coding: utf-8 -*-

from multiprocessing import Process, Array, Value, Lock, BoundedSemaphore, Semaphore
from random import randint

NPROD = 5 # numero de productores
PROC = 8 # numero de procesos
# numero de consumidores siempre 1

"""
 lst = lista de procesos running de bool que inicialmente estan a true
 
 consumidor -> espero a que todos hallan producido (wait)
 while algun valor de lst sea true :
 loop
     - todos los productores han producido
     - procesar el minimo (si vale -1 le descarto, ese proceso acabo)
     - ¿que proceso le ha producido? El p
     if[ calcular posicion ]:
     - signal(p) -> tiene que producir otro valor (espero)
     - wait(p)
 
 
 """
def producer(pid, buffer, running, empty, non_empty): # cada productor produce de uno en uno
	for i in range(PROC):
		empty[pid].acquire()
		buffer[pid] += randint(0, 5)
		non_empty[pid].release()
     
	buffer[pid] = -1
	running[pid] = False
    
def consumer(consumed, buffer, running, empty, non_empty):
	# espero a que todos los productores hayan producido
	for i in non_empty:
		i.acquire()
	while any(running): # mientras haya procesos...
		p = minimum_index(buffer) # procesar el minimo, necesito saber QUE proceso lo ha producido (indice)
		consumed.append(buffer[p])
		empty[p].release() # hay que producir otro
     	
     
def minimum_index(buffer):
	positives = [i for i in buffer if i>=0] # me olvido de los -1
	lst = list(buffer)
	return lst.index(min(positives)) # posicion del minimo del buffer


def main():
	running = Array('b',[True for i in range(NPROD)])
	buffer = Array('i',[0]*NPROD)
	empty = [BoundedSemaphore(1) for i in range(NPROD)] # lista de semaforos, uno por productor
	non_empty = [Semaphore(0) for i in range(NPROD)]
	consumed = []
	lp = []
    # Productores:
	for pid in range(NPROD):
		lp.append(Process(target = producer, args=(pid, buffer, running, empty, non_empty)))
    
    # Consumidor:
	lp.append(Process(target = consumer, args=(consumed, buffer, running, empty, non_empty)))
    
	for p in lp:
		p.start()
	for p in lp:
		p.join()
        
if __name__=='__main__':
	main()
