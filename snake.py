import csv
import numpy as np
import copy
import sys
import fileinput # remove duplicates
import os


#REMOVE OLDER FILES -------------------------------------------
myfile="output.csv"
## if file exists, delete it ##
if os.path.isfile(myfile):
    os.remove(myfile)
else:    ## Show an error ##
    print("Error: %s file not found" % myfile)




# The user has to put the .csv file in the argument of script like:
# >>>python3 snake.py snake_csv.csv
filename = sys.argv[-1]


# Reading of the matrix of csv file

output = csv.writer(open("output.csv", "a"))
TAMANHO = 0 #size of the matrix to be read

# Open the input file, take the size of the matrix, and use a Binario matrix to take places where have already read
with open(filename, 'rb') as f:
	reader = csv.reader(open(filename, 'rU'), dialect=csv.excel_tab,delimiter=',')
	reader2 = csv.reader(open(filename, 'rU'), dialect=csv.excel_tab,delimiter=',')
	i=0
	j=0
	N = len(list(reader2))
	TAMANHO = N
	shape = (N,N)

	matrix = np.empty(shape)
	binario = np.empty(shape)

	for row in reader:
		i=0
		for col in row:
			matrix[i][j] = col
			binario[i][j] = 0
			i = i+1
		j=j+1
	
# Put zero(0) in all cell of the matrix
def zeraMatriz(A):
	for i in range(0,TAMANHO):
		for j in range(0, TAMANHO):
			A[i,j]=0

def init(A, B,FINAL, j, i, c, S, text, jBefore, iBefore):

	#put in output file, when find a complete 7snake size their cells and sum 
	if(c==7):
		FINAL[j][i]=1
		output.writerow([text, S])
		return
	else:
		text = text + ' ,' + str(i) + '#' + str(j)
		S = S + A[j][i]
		shape = (TAMANHO, TAMANHO)
		d=np.empty(shape)
		e=np.empty(shape)
		f=np.empty(shape)
		g=np.empty(shape)
		if((j-1) >= 0):
			if((str(j-1)+'#'+str(i)) != ((str(jBefore)+'#')+str(iBefore))):
				d = B[:][:]
				d[i][j]=1
				init(A, d,FINAL, j-1, i, c+1, S, text, j, i)
		if((i-1) >= 0):
			if((str(j)+'#'+str(i-1)) != ((str(jBefore)+'#')+str(iBefore))):
				e = B[:][:]
				e[i][j]=1
				init(A, e,FINAL, j, i-1, c+1, S, text, j, i)
		if((i+1) < TAMANHO):
			if((str(j)+'#'+str(i+1)) != ((str(jBefore)+'#')+str(iBefore))):
				f = B[:][:]
				f[i][j]=1
				init(A, f,FINAL, j, i+1, c+1, S, text, j, i)	
		if((j+1) < TAMANHO):
			if((str(j+1)+'#'+str(i)) != ((str(jBefore)+'#')+str(iBefore))):		
				g = B[:][:]
				g[i][j]=1
				init(A, g,FINAL, j+1, i, c+1, S, text, j, i)

# run for all cell, looking for all snakes
for i in range(0,TAMANHO):
		for j in range(0, TAMANHO):
			init(matrix, binario,binario, j,i, 0, 0,"",-1,-1)
	

#remove snakes duplicated and put in another file
with open('output.csv','r') as in_file, open('removedDuplicated.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate
        seen.add(line)
        out_file.write(line)

# second part of reading
# reading and comparing with others snakes to know if does not pass above the other
phrases1 = csv.reader(open('removedDuplicated.csv', 'rU'), dialect=csv.excel_tab,delimiter=',')
phrases2 = csv.reader(open('removedDuplicated.csv', 'rU'), dialect=csv.excel_tab,delimiter=',')
consulta = csv.reader(open('removedDuplicated.csv', 'rU'), dialect=csv.excel_tab,delimiter=',')
total_p = len(list(phrases1))

shape2 = (total_p,2)
snakes = np.empty(shape2)


def isRepeated(vetor):
	y=[i for i, x in enumerate(vetor) if vetor.count(x) >1]
	# print(y)
	if(len(y)>0):
		return True
		# print("tem repetido itens")

def trimList(lista):
	stripped = [line.strip() for line in lista]
	return stripped



def lookMatch():
	find=False
	pj=0
	soma=0
	for item in phrases2:
		# print(item)
		pi=0
		for col in item:
			if(pi==0):
				a1 = col
				a = col.split(',')
				for cell in a:
					v = cell.split('#')
			if(pi==1):
				soma = col
				for con in consulta:
					t=0
					for coluna in con:
						if(t==0):

							a2 = coluna.split(',')
							if(isRepeated(a2)):
								guarda = -1
							else:
								guarda = coluna
						if(t==1):
							if(coluna == soma):

								juntarDuasListas = a2 + a
								juntarDuasListas.remove(' ')

								a = trimList(a)
								a2 = trimList(a2)
								list2 = trimList(juntarDuasListas)
								if(isRepeated(list2)):
									z = True
								else:
									print('------------------')
									print ("Matching")
							
									print(a)
									print(a2)
									find = True
									return (find) # if you want to find more than one snakes comment this line
						t = t + 1	
			pi=pi+1
		pj=pj+1	
	return (find)	

existSnakesEqual = lookMatch()	
if (existSnakesEqual==False):
	print("Does not exist two snakes with the same Sum")