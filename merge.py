# -*- coding: utf-8 -*-

from multiprocessing import Process, Array, Value, Lock, BoundedSemaphore, Semaphore
from random import randint

NPROD = 3 # numero de productores
PROC = 10 # numero de procesos
# numero de consumidores siempre 1

def producer(pid, buffer, running, empty, non_empty, lock): # cada productor produce de uno en uno
	for i in range(PROC):
		empty[pid].acquire()
		
		lock.acquire()
		print(f"Esta produciendo el productor {pid}")
		buffer[pid] += randint(0, 5)
		lock.release()
		
		non_empty[pid].release()
		print(f"Ha terminado de producir el productor {pid}")
	buffer[pid] = -1
    
def consumer(consumed, buffer, empty, non_empty, lock):
	# espero a que todos los productores hayan producido
	for i in non_empty:
		i.acquire()
	
	p = minimum_index(buffer)
	running = p == -1
	while not running: # mientras haya procesos...
		lock.acquire()
		consumed.append(buffer[p]) # lo consumo
		print(f"Consumiendo... {buffer[p]}")
		lock.release()
		
		empty[p].release() # hay que producir otro
		non_empty[p].acquire()
		
		lock.acquire()
		p = minimum_index(buffer) # pasamos a consumir el siguiente
		running = p == -1
		lock.release()
	print(f"Consumidos... {consumed}")
     
def minimum_index(buffer):
	positives = [i for i in buffer if i>=0] # me olvido de los -1
	if not positives: 
		return -1
	lst = list(buffer)
	return lst.index(min(positives)) # posicion del minimo del buffer


def main():
	buffer = Array('i',[0]*NPROD)
	empty = [BoundedSemaphore(1) for i in range(NPROD)] # lista de semaforos, uno por productor
	non_empty = [Semaphore(0) for i in range(NPROD)]
	lock = Lock()
	consumed = []
	lp = []
    # Productores:
	for pid in range(NPROD):
		lp.append(Process(target = producer, args=(pid, buffer, running, empty, non_empty, lock)))
    
    # Consumidor:
	lp.append(Process(target = consumer, args=(consumed, buffer, empty, non_empty, lock)))
    
	for p in lp:
		p.start()
	for p in lp:
		p.join()
        
if __name__=='__main__':
	main()
