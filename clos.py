import numpy
import random
import sys

orig_stdout = sys.stdout
f = file('output.txt', 'w')
sys.stdout = f




n=16
r=16
q=4
IM=numpy.zeros((n/q,q,2*q-1))
CM=numpy.zeros((2*q-1,n/q,r/q))
OM=numpy.zeros((n/q,q,2*q-1))
PCount=numpy.zeros(n)
MCount=numpy.zeros(r)
x=0
y=0
z=0

def debug():
	print "\nIM:",IM
	print "\nCM:",CM
	print "\nOM:",OM
	#print PCount
	print "\nMem Double requests:",MCount


def add(PE,ME):
	if(1 in IM[PE/q,PE%q]):
		PCount[PE]+=1
	elif(1 in OM[ME/q,ME%q]):
		MCount[ME]+=1
	else:
		x=0
		while(1 in IM[PE/q,:,x] or 1 in OM[ME/q,:,x] or 1==CM[x,PE/q,ME/q]):
			x+=1  #If blocked, x would increment past 2q-1, throwing an error
		IM[PE/q,PE%q,x]=1
		OM[ME/q,ME%q,x]=1
		CM[x,PE/q,ME/q]=1

def remove(PE,ME):
	if(1 in IM[PE/q,PE%q] and 1 in OM[ME/q,ME%q]):
		for x in range(2*q-1):
			if(IM[PE/q,PE%q,x]==OM[ME/q,ME%q,x] and OM[ME/q,ME%q,x]==CM[x,PE/q,ME/q]):
				IM[PE/q,PE%q,x]=0
				OM[ME/q,ME%q,x]=0
				CM[x,PE/q,ME/q]=0

			

def genRequests(ad,rm):
	ca=0
	cr=0
	while(ca < ad and cr < rm):
		#print ca+cr
		if(ca==ad):
			cr+=1
			remove(random.randint(0,15),random.randint(0,15))
		elif(cr==rm):
			ca+=1
			add(random.randint(0,15),random.randint(0,15))
		else:
			if(random.randint(0,ad+rm)>ad):
				cr+=1
				remove(random.randint(0,15),random.randint(0,15))
			else:
				ca+=1
				add(random.randint(0,15),random.randint(0,15))
		



genRequests(10000,1000)
debug()

sys.stdout = orig_stdout
f.close()