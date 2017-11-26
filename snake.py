import csv
import numpy as np
import copy
import sys
import fileinput # remove duplicates

filename = sys.argv[-1]

# leitura de matrix do arquivo csv
# dada uma linha e coluna, criar possiveis snakes para aquela posicao e calcular sua soma

output = csv.writer(open("output.csv", "a"))
TAMANHO = 0
contador = 0

with open(filename, 'rb') as f:
	# reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\r')
	# reader = csv.reader(f, dialect=csv.excel_tab)
	reader = csv.reader(open(filename, 'rU'), dialect=csv.excel_tab,delimiter=',')
	reader2 = csv.reader(open(filename, 'rU'), dialect=csv.excel_tab,delimiter=',')
	# dialect=csv.excel_tab
	i=0
	j=0
	N = len(list(reader2))
	TAMANHO = N
	shape = (N,N)

	# matrix=[10][10]
	matrix = np.empty(shape)
	binario = np.empty(shape)

	for row in reader:
		i=0
		for col in row:
			# print str(i) + "," + str(j) + " = " + str(col)
			# matrix[j][i] = col
			# print col + "#"
			matrix[i][j] = col
			binario[i][j] = 0
			i = i+1
		j=j+1
	# print matrix	
	# print binario


# for linha in range(0,N):
	# for coluna in range(0,N):
		# print str(linha) + ' ' + str(coluna)

# print matrix[1][3]

def zeraMatriz(A):
	for i in range(0,TAMANHO):
		for j in range(0, TAMANHO):
			A[i,j]=0

def init(A, B,FINAL, j, i, c, S, text, jBefore, iBefore):

	# print np.sum(A)

	if(c==7):
		# print B
		# print S
		# print c
		# print text
		FINAL[j][i]=1
		# print B
		# zeraMatriz(B)

		output.writerow([text, S])
		# print '-------------------------------------------'
		
		# contador = contador +1
		# print ('contador: ' + str(contador))
		return
	else:
		text = text + ' ,' + str(i) + '#' + str(j)
		# B[i][j]=1
		# print 'SOMA S + A[ij]: ' + str(S) + ' + ' + str(A[j][i]) + ' = '+ str(S+A[j][i])
		S = S + A[j][i]
		shape = (TAMANHO, TAMANHO)
		d=np.empty(shape)
		e=np.empty(shape)
		f=np.empty(shape)
		g=np.empty(shape)
		# if((j-1) > 0 and B[i][j-1]==0):
		if((j-1) >= 0):	
			# B[i][j-1]=1
			if((str(j-1)+'#'+str(i)) != ((str(jBefore)+'#')+str(iBefore))):
				d = B[:][:]
				d[i][j]=1
				init(A, d,FINAL, j-1, i, c+1, S, text, j, i)
		# if((i-1) > 0 and B[i-1][j]==0):
		if((i-1) >= 0):
			# B[i-1][j]=1
			if((str(j)+'#'+str(i-1)) != ((str(jBefore)+'#')+str(iBefore))):
				e = B[:][:]
				e[i][j]=1
				init(A, e,FINAL, j, i-1, c+1, S, text, j, i)
		# if((i+1) < TAMANHO and B[i+1][j]==0):
		if((i+1) < TAMANHO):
			# B[i+1][j]=1
			if((str(j)+'#'+str(i+1)) != ((str(jBefore)+'#')+str(iBefore))):
				f = B[:][:]
				f[i][j]=1
				init(A, f,FINAL, j, i+1, c+1, S, text, j, i)	
		# if((j+1) < TAMANHO and B[i][j+1]==0):
		if((j+1) < TAMANHO):
			# B[i][j+1]=1
			if((str(j+1)+'#'+str(i)) != ((str(jBefore)+'#')+str(iBefore))):		
				g = B[:][:]
				g[i][j]=1
				init(A, g,FINAL, j+1, i, c+1, S, text, j, i)
#do just for the firt cell - test
palavra = str("")
# init(matrix, binario,binario, 0,0, 0, 0,palavra)

for i in range(0,TAMANHO):
		for j in range(0, TAMANHO):
			init(matrix, binario,binario, j,i, 0, 0,palavra,-1,-1)

#do for all cells
# for i in range(0,TAMANHO):
# 		for j in range(0, TAMANHO):
# 			init(matrix, binario,binario, j,i, 0, 0,palavra)
	

#remove duplicated
with open('output.csv','r') as in_file, open('outputFinal.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)


#second part of reading
phrases1 = csv.reader(open('outputFinal.csv', 'rU'), dialect=csv.excel_tab,delimiter=',')
phrases2 = csv.reader(open('outputFinal.csv', 'rU'), dialect=csv.excel_tab,delimiter=',')
consulta = csv.reader(open('outputFinal.csv', 'rU'), dialect=csv.excel_tab,delimiter=',')
total_p = len(list(phrases1))
# print (total_p)	

shape2 = (total_p,2)
snakes = np.empty(shape2)
# dict={}
# sorted_array = np.argsort(snakes,axis=0,kind='quicksort', order=None)
# sorted_array = np.sort(snakes)
# snakes = snakes[snakes[:,1].argsort()]

def isRepeated(vetor):
	y=[i for i, x in enumerate(vetor) if vetor.count(x) >1]
	# print(y)
	if(len(y)>0):
		return True
		# print("tem repetido itens")

def trimList(lista):
	stripped = [line.strip() for line in lista]
	return stripped

pj=0
soma=0
for item in phrases2:
	# print(item)
	pi=0
	for col in item:
		if(pi==0):
			a1 = col
			a = col.split(',')
			# print (a)
			for cell in a:
				v = cell.split('#')
				# print (v)
		if(pi==1):
			soma = col
			# print(col)
			for con in consulta:
				t=0
				for coluna in con:
					if(t==0):

						a2 = coluna.split(',')
						if(isRepeated(a2)):
							guarda = -1
						else:
						# print(a2)
							guarda = coluna
					if(t==1):
						# print(coluna)
						if(coluna == soma):

							# a2.remove(' ')
							# a.remove('')
							juntarDuasListas = a2 + a
							juntarDuasListas.remove(' ')

							a = trimList(a)
							a2 = trimList(a2)
							list2 = trimList(juntarDuasListas)
							# print(list2)
							if(isRepeated(list2)):
								z = True
							else:
								print('------------------')
								print ("Matching")
								print(a)
								print(a2)
								# print(coluna)
								# print(item)
								# print(con)
								# print(guarda)
					t = t + 1	
		# print(item)
		# snakes[pi][pj] = col	
		pi=pi+1
	pj=pj+1	