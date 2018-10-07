import copy
import random

import Colors as color

'''
Battaglia Navale giocatore vs PC
Sviluppato da Fabio Somaglia e Davide Locatelli per progetto di Interazione Uomo Macchina
'''

# computer_brain è una matrice, inizializzata con valori None, che salva tutti dati delle giocate del computer in
# modo da fargli prendere decisioni simili a una persona

computer_brain = [[None for col in range(7)] for row in range(5)]
computer_brain[0][0] = "Portaerei"
computer_brain[0][1] = False  # con False colpisco a sinistra/su, con True colpisco a destra/giù
computer_brain[1][0] = "Corazzata"
computer_brain[1][1] = False
computer_brain[2][0] = "Sottomarino"
computer_brain[2][1] = False
computer_brain[3][0] = "Incrociatore"
computer_brain[3][1] = False
computer_brain[4][0] = "Motovedetta"
computer_brain[4][1] = False


# metodo che si occupa di stampare il campo da gioca del giocatore e del computer
def stampa_campo(s, campo):
	if s == "u":
		giocatore = "SOLDATO"
	else:
		giocatore = "COMPUTER"

	print("\n" + color.colors.fg.green + color.colors.bold + "\t\t\t\tQuesto è il campo del " + giocatore + color.colors.reset)

	# stampa i numeri orizzontali
	print(" ", end=' ')
	for i in range(10):
		print("  " + str(i + 1) + "  ", end=' ')
	print("\n")

	for i in range(10):
		# stampa le linee verticali del campo
		if i != 9:
			print(str(i + 1) + "  ", end=' ')
		else:
			print(str(i + 1) + " ", end=' ')

		# stampa i bordi divisori e i valori all'interno delle celle
		for j in range(10):
			if campo[i][j] == -1:
				print(' ', end=' ')
			elif s == "u":
				if campo[i][j] == '*':
					print(color.colors.fg.lightblue + campo[i][j] + color.colors.reset, end=' ')
				elif campo[i][j] == 'X':
					print(color.colors.fg.red + campo[i][j] + color.colors.reset, end=' ')
				else:
					print(color.colors.fg.yellow + campo[i][j] + color.colors.reset, end=' ')
			elif s == "c":
				if campo[i][j] == '*':
					print(color.colors.fg.lightblue + campo[i][j] + color.colors.reset, end=' ')
				elif campo[i][j] == 'X':
					print(color.colors.fg.red + campo[i][j] + color.colors.reset, end=' ')
				else:
					print(" ", end=' ')

			if j != 9:
				print(" | ", end=' ')
		print()

		# stampa la linea orizzontale del campo
		if i != 9:
			print("   ----------------------------------------------------------")
		else:
			print()


# metodo che si occupa di far scegliere al giocatore dove posizionare le navi
def posiziona_navi_giocatore(campo, navi):
	for nave in navi.keys():
		# ottengo le coordinate dal giocatore e confermo le posizioni delle navi
		posizione_valida = False
		while not posizione_valida:
			stampa_campo("u", campo)
			print("Stai per posizionare: " + nave)
			x, y = get_coordinate()
			orientamento = get_orientamento()
			posizione_valida = controllo(campo, navi[nave], x, y, orientamento)
			if not posizione_valida:
				print("Non posso inserire una nave in quelle coordinate.\nRiprova a inserirle.")
				input("Premi INVIO per continuare.")

		# posiziono la nave
		campo = posiziona_nave_orientamento(campo, navi[nave], nave[0], orientamento, x, y)
	stampa_campo("u", campo)

	input("Abbiamo finito di posizionare le navi. Clicca INVIO per cominciare la partita.")
	return campo


# metodo che si occupa di posizionare random le navi del computer
def posiziona_navi_computer(campo, navi):
	for nave in navi.keys():
		# genero coordinate random e controllo che la posizione sia corretta per poter inserire la nave
		valido = False
		while not valido:
			x = random.randint(1, 10) - 1
			y = random.randint(1, 10) - 1
			o = random.randint(0, 1)
			if o == 0:
				orientamento = "v"
			else:
				orientamento = "o"
			valido = controllo(campo, navi[nave], x, y, orientamento)

		# posiziono la nave del computer
		print("Il computer sta posizionando: " + nave)
		campo = posiziona_nave_orientamento(campo, navi[nave], nave[0], orientamento, x, y)
	return campo


# metodo che si occupa effettivamente di posizionare, in base all'orientamento stabilito dal random, le navi del
# computer
def posiziona_nave_orientamento(campo, nave, s, orientamento, x, y):
	if orientamento == "v":
		for i in range(nave):
			campo[x + i][y] = s
	elif orientamento == "o":
		for i in range(nave):
			campo[x][y + i] = s
	return campo


# metodo che controlla se la nave può essere inserita in quelle coordinate
def controllo(campo, nave, x, y, orientamento):
	if orientamento == "v" and x + nave > 10:
		return False
	elif orientamento == "o" and y + nave > 10:
		return False
	else:
		if orientamento == "v":
			for i in range(nave):
				if campo[x + i][y] != -1:
					return False
		elif orientamento == "o":
			for i in range(nave):
				if campo[x][y + i] != -1:
					return False
	return True


# metodo che chiede al giocatore in quale orientamento vuole posizionare la nave
def get_orientamento():
	while True:
		user_input = input("Verticale o orizzontale? (v/o): ")
		if user_input == "v" or user_input == "o":
			return user_input
		else:
			print("Errore! Si deve inserire 'v' oppure 'o'")


# metodo che chiede al giocatore in quali coordinate posizionare la nave
def get_coordinate():
	while True:
		input_giocatore = input("Inserisci le coordinate (riga,colonna): ")
		try:
			# controllo che i dati inseriti dal giocatore siano separati da delle virgole
			coor = input_giocatore.split(",")
			if len(coor) != 2:
				raise Exception("Input errato. Hai scritto troppo o troppo poco.");

			# controllo che i 2 input siano dei numeri
			coor[0] = int(coor[0]) - 1
			coor[1] = int(coor[1]) - 1

			# controllo che i due input siano entrambi numeri compresi tra 1 e 10
			if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
				raise Exception("Input errato. Inserire dei numeri tra 1 e 10.")

			# ritorno le coordinate
			return coor

		except ValueError:
			print("Input errato. Si prega di inserire solo valori numerici")
		except Exception as e:
			print(e)


# metodo che anticipa la riuscita di una mossa, utile in quanto se restituisce riprova significa che si è cercato di
# colpire una coordinata già selezionata in precedenza
def fai_mossa(campo, x, y):
	if campo[x][y] == -1:
		return "mancato"
	elif campo[x][y] == '*' or campo[x][y] == 'X':
		return "riprova"
	else:
		return "colpito"


# metodo che ottiene le coordinate dall'utente e controllo se è stata colpita o meno una nave, se è stata colpita,
# controllo se è stata affondata o se il giocatore ha vinto la partita
def mossa_giocatore(campo):
	print("\n" + color.colors.bg.blue + color.colors.fg.yellow + "Turno del SOLDATO" + color.colors.reset)
	while True:
		x, y = get_coordinate()
		risultato = fai_mossa(campo, x, y)
		if risultato == "colpito":
			print(color.colors.fg.red + "Hai colpito la nave avversaria nella posizione " + str(x + 1) + "," + str(y + 1) + color.colors.reset)
			controlla_affondato(campo, x, y)
			campo[x][y] = 'X'
			if controlla_vittoria(campo):
				stampa_campo("c", campo)
				return "VITTORIA"
		elif risultato == "mancato":
			print(color.colors.fg.lightblue + "Hai colpito l'oceano nelle coordinate " + str(x + 1) + "," + str(y + 1) + color.colors.reset)
			campo[x][y] = "*"
		elif risultato == "riprova":
			print("Hai già sparato in quella coordinata. Riprova!")
		if risultato != "riprova":
			return campo


# metodo che si occupa della giocata del computer, salva e utilizza i dati nella matrice computer_brain per prendere
# decisioni sulla giocata in modo simili a un umano
def mossa_computer(campo):
	indice_nave = -1  # per sapere a che nave ci riferiamo quando si salva o si legge da computer_brain

	# True: computer non conosce navi da affondare, quindi spara random. False: il computer è a conoscenza che deve
	# affondare una nave già colpita in almeno un punto
	spara_random = True

	risultato = None  # return del metodo fai_mossa()

	print("\n" + color.colors.bg.blue + color.colors.fg.yellow + "Turno del COMPUTER" + color.colors.reset)

	i = 0
	flag = False
	while i < 5 and flag == False:  # controllo se è presente una nave già colpita e da affondare
		# se entro qui significa che c'è una nave da affondare
		if computer_brain[i][3] != None:
			# print("Il pc ha capito che c'è una nave da affondare")
			indice_nave = i
			spara_random = False  # siccome c'è una nave da affondare, non sparo più random, ma faccio ragionare il pc
			x = computer_brain[i][3]  # riga
			y = computer_brain[i][4]  # colonna
			flag = True  # esco appena trovo la prima nave colpita
		i += 1

	if spara_random:  # se non è stata colpita nessuna nave in precedenza, sparo random
		while True:
			x = random.randint(1, 10) - 1
			y = random.randint(1, 10) - 1
			risultato = fai_mossa(campo, x, y)
			if risultato == "colpito":
				print(color.colors.fg.red + "Il COMPUTER ti ha colpito nella posizione " + str(x + 1) + "," + str(y + 1) + color.colors.reset)
				indice_nave, affondata = controlla_affondato(campo, x, y)
				# print("L'indice della nave è " + str(indice_nave) + " Affondata? " + str(affondata))
				if not affondata:
					# print("Il pc ha colpito una nave per la prima volta")
					# salvo le coordinate quando colpisco una nave
					computer_brain[indice_nave][3] = x
					computer_brain[indice_nave][4] = y
					computer_brain[indice_nave][5] = affondata
				else:
					# print("il pc ha affondato una nave")
					# elimino le coordinate in quanto la nave è stata affondata
					computer_brain[indice_nave][3] = None
					computer_brain[indice_nave][4] = None
					computer_brain[indice_nave][5] = affondata

				campo[x][y] = 'X'
				if controlla_vittoria(campo):
					stampa_campo("u", campo)
					return "VITTORIA"
			elif risultato == "mancato":
				print(color.colors.fg.lightblue + "Il COMPUTER ha colpito l'oceano nelle coordinate " + str(x + 1) + "," + str(y + 1) + color.colors.reset)
				campo[x][y] = "*"

			if risultato != "riprova":
				return campo
	else:  # se è stata già colpita almeno una nave in precedenza, il computer tenta di affondarla
		while True:
			if computer_brain[indice_nave][2] == "orizzontale":  # se sappiamo già l'orientamento della nave
				# print("orizz")
				colonna_sx = min(computer_brain[indice_nave][4], computer_brain[indice_nave][6])
				colonna_dx = max(computer_brain[indice_nave][4], computer_brain[indice_nave][6])
				# print("colonna sx dx " + str(colonna_sx + 1) + " " + str(colonna_dx + 1))

				if computer_brain[indice_nave][1] == False:  # sparo a sinistra
					# print("mi posiziono a sinistra")
					if colonna_sx - 1 >= 0:
						y = colonna_sx - 1
						# print("nuova colonna dopo il posizionamento a sinistra " + str(y + 1))
					else:
						computer_brain[indice_nave][1] = True
						# print("mi devo spostare a destra in quanto a sinistra non posso più")
				if computer_brain[indice_nave][1] == True:  # sparo a destra
					# print("mi posiziono a destra")
					if colonna_dx + 1 <= 9:
						y = colonna_dx + 1
						# print("nuova colonna dopo il posizionamento a destra " + str(y + 1))

				# print("faccio la mossa con le coord " + str(x + 1) + "," + str(y + 1))
				risultato = fai_mossa(campo, x, y)
				nave_originale = indice_nave
				if risultato == "colpito":
					indice_nave, affondata = controlla_affondato(campo, x, y)
					if nave_originale == indice_nave:  # se ho colpito la stessa nave
						# print("ho colpito la stessa nave")
						if affondata:
							# cancello le coordinate quando affondo una nave
							computer_brain[indice_nave][3] = None
							computer_brain[indice_nave][4] = None
							computer_brain[indice_nave][5] = affondata
						else:
							# se False, salvo il nuovo estremo della nave nella cella dedicata all'estremo sinistro
							if computer_brain[indice_nave][1] == False:
								computer_brain[indice_nave][4] = y  # salvo la nuova colonna
							else:  # altrimenti lo salvo nella cella dedicata all'estremo destro
								computer_brain[indice_nave][6] = y  # salvo la nuova colonna
							computer_brain[indice_nave][5] = affondata
					else:
						# print("non ho colpito la stessa nave in orizzontale")
						if affondata:
							# cancello le coordinate quando affondo una nave
							computer_brain[indice_nave][3] = None
							computer_brain[indice_nave][4] = None
							computer_brain[indice_nave][5] = affondata
						else:
							computer_brain[indice_nave][3] = x
							computer_brain[indice_nave][4] = y
							computer_brain[indice_nave][5] = affondata

					campo[x][y] = 'X'
					if controlla_vittoria(campo):
						stampa_campo("u", campo)
						return "VITTORIA"

				elif risultato == "mancato":
					computer_brain[indice_nave][1] = True
					print(color.colors.fg.lightblue + "Il COMPUTER ha colpito l'oceano nelle coordinate " + str(
						x + 1) + "," + str(y + 1) + color.colors.reset)
					campo[x][y] = "*"

				elif risultato == "riprova":
					computer_brain[indice_nave][
						1] = True  # se ha sinistra non ho più niente da colpire, inizio a sparare a destra

				if risultato != "riprova" and risultato != None:
					return campo

			elif computer_brain[indice_nave][2] == "verticale":
				# print("verti")
				riga_su = min(computer_brain[indice_nave][3], computer_brain[indice_nave][6])
				riga_giu = max(computer_brain[indice_nave][3], computer_brain[indice_nave][6])
				# print("riga su giù " + str(riga_su + 1) + " " + str(riga_giu + 1))

				if computer_brain[indice_nave][1] == False:  # sparo su
					# print("mi posiziono su")
					if riga_su - 1 >= 0:
						x = riga_su - 1
						# print("nuova riga dopo il posizionamento in su " + str(x + 1))
					else:
						computer_brain[indice_nave][1] = True
						# print("mi devo spostare in giù in quanto in su non posso più")
				if computer_brain[indice_nave][1] == True:  # sparo giù
					# print("mi posiziono giù")
					if riga_giu + 1 <= 9:
						x = riga_giu + 1
						# print("nuova riga dopo il posizionamento in giù " + str(x + 1))

				# print("faccio la mossa con le coord " + str(x + 1) + "," + str(y + 1))
				risultato = fai_mossa(campo, x, y)
				nave_originale = indice_nave
				if risultato == "colpito":
					indice_nave, affondata = controlla_affondato(campo, x, y)
					if nave_originale == indice_nave:
						if affondata:
							computer_brain[indice_nave][3] = None
							computer_brain[indice_nave][4] = None
							computer_brain[indice_nave][5] = affondata
						else:
							if computer_brain[indice_nave][1] == False:
								computer_brain[indice_nave][3] = x
							else:
								computer_brain[indice_nave][6] = y
							computer_brain[indice_nave][5] = affondata
					else:
						# print("non ho colpito la stessa nave in verticale")
						if affondata:
							computer_brain[indice_nave][3] = None
							computer_brain[indice_nave][4] = None
							computer_brain[indice_nave][5] = affondata
						else:
							computer_brain[indice_nave][3] = x
							computer_brain[indice_nave][4] = y
							computer_brain[indice_nave][5] = affondata

					campo[x][y] = 'X'
					if controlla_vittoria(campo):
						stampa_campo("u", campo)
						return "VITTORIA"

				elif risultato == "mancato":
					computer_brain[indice_nave][1] = True
					print(color.colors.fg.lightblue + "Il COMPUTER ha colpito l'oceano nelle coordinate " + str(
						x + 1) + "," + str(y + 1) + color.colors.reset)
					campo[x][y] = "*"

				elif risultato == "riprova":
					computer_brain[indice_nave][
						1] = True  # se in su non ho più niente da colpire, inizio a sparare in giù

				if risultato != "riprova" and risultato != None:
					return campo

			# se invece non so ancora l'orientamento della nave colpita, sparo random nei suoi punti cardinali
			else:
				coord = random.randint(1, 4)  # random Nord, Sud, Est, Ovest
				# print("Sto cercando la nave a " + str(coord))
				# print("Riga: " + str(x + 1) + " Colonna: " + str(y + 1))
				xC, yC = x, y
				if coord == 1:  # sparo a Nord
					xC = x - 1
					# controllo che x sia compreso tra 1 e 10
					if xC <= 9 and xC >= 0:
						# print("Provo a sparare più a Nord")
						risultato = fai_mossa(campo, xC, y)
				elif coord == 2:  # sparo a Sud
					xC = x + 1
					if xC <= 9 and xC >= 0:
						# print("Provo a sparare più a Sud")
						risultato = fai_mossa(campo, xC, y)
				elif coord == 3:  # sparo a Est
					yC = y + 1
					if yC <= 9 and yC >= 0:
						# print("Provo a sparare più a Est")
						risultato = fai_mossa(campo, x, yC)
				elif coord == 4:  # sparo a Ovest
					yC = y - 1
					if yC <= 9 and yC >= 0:
						# print("Provo a sparare più a Ovest")
						risultato = fai_mossa(campo, x, yC)

				# guardiamo se la nave è la stessa, quindi riusciamo a scrivere l'orientamento e le nuove coordinate.
				# Se la nave è differente, scriviamo solo le cooordinate
				if risultato == "colpito":
					print(color.colors.fg.red + "Il COMPUTER ti ha colpito nella posizione " + str(xC + 1) + "," + str(yC + 1) + color.colors.reset)

					nave_originale = indice_nave
					# qui controllo se la nave colpita è la stessa di nave_originale
					indice_nave, affondata = controlla_affondato(campo, xC, yC)

					if nave_originale == indice_nave:  # se la nave che ho colpito adesso è uguale a quella colpita prima
						if affondata:
							computer_brain[indice_nave][3] = None
							computer_brain[indice_nave][4] = None
							computer_brain[indice_nave][5] = affondata
						elif coord == 2 or coord == 1:
							computer_brain[indice_nave][2] = "verticale"  # possiamo dedurne l'orientamento
							estremo_minimo = min(computer_brain[indice_nave][3], xC)
							estremo_massimo = max(computer_brain[indice_nave][3], xC)
							computer_brain[indice_nave][3] = estremo_minimo  # salvo le coord dell'estremo su della nave
							computer_brain[indice_nave][
								6] = estremo_massimo  # salvo le coord dell'estremo giù della nave
						elif coord == 3 or coord == 4:
							computer_brain[indice_nave][2] = "orizzontale"
							estremo_minimo = min(computer_brain[indice_nave][4], yC)
							estremo_massimo = max(computer_brain[indice_nave][4], yC)
							computer_brain[indice_nave][
								4] = estremo_minimo  # salvo le coord dell'estremo sinistro della nave
							computer_brain[indice_nave][
								6] = estremo_massimo  # salvo le coord dell'estremo destro della nave
					elif affondata:
						computer_brain[indice_nave][3] = None
						computer_brain[indice_nave][4] = None
						computer_brain[indice_nave][5] = affondata
					else:
						# salvo le coordinate della nave che ho colpito al secondo tiro
						computer_brain[indice_nave][3] = xC
						computer_brain[indice_nave][4] = yC
						computer_brain[indice_nave][5] = affondata

					campo[xC][yC] = 'X'
					if controlla_vittoria(campo):
						stampa_campo("u", campo)
						return "VITTORIA"

				elif risultato == "mancato":
					print(color.colors.fg.lightblue + "Il COMPUTER ha colpito l'oceano nelle coordinate " + str(
						xC + 1) + "," + str(yC + 1) + color.colors.reset)
					campo[xC][yC] = "*"

				if risultato != "riprova" and risultato != None:  # se risultato è None, riprova a sparare in un'altra coordinata
					return campo


'''
# metodo che si occupa della giocata del computer, ma senza il ragionamento nell'effettuare una mossa
def mossa_computer_senza_ai(campo):
	print("\n" + color.colors.bg.blue + color.colors.fg.yellow + "Turno del COMPUTER" + color.colors.reset)
	while (True):
		x = random.randint(1, 10) - 1
		y = random.randint(1, 10) - 1
		risultato = fai_mossa(campo, x, y)
		if risultato == "colpito":
			print(color.colors.fg.red + "Il COMPUTER ti ha colpito nella posizione " + str(x + 1) + "," + str(y + 1) + color.colors.reset)
			controlla_affondato(campo, x, y)
			campo[x][y] = 'X'
			if controlla_vittoria(campo):
				return "VITTORIA"
		elif risultato == "mancato":
			print(color.colors.fg.lightblue + "Il COMPUTER ha colpito l'oceano nelle coordinate " + str(x + 1) + "," + str(y + 1) + color.colors.reset)
			campo[x][y] = "*"

		if risultato != "riprova":
			return campo
'''


# metodo che restituisce quale nave è stata colpita e se è stata affondata
def controlla_affondato(campo, x, y):
	if campo[x][y] == "P":
		nave = "Portaerei"
		pos = 0  # serve per l'indice nel computer_brain
	elif campo[x][y] == "C":
		nave = "Corazzata"
		pos = 1
	elif campo[x][y] == "S":
		nave = "Sottomarino"
		pos = 2
	elif campo[x][y] == "I":
		nave = "Incrociatore"
		pos = 3
	elif campo[x][y] == "M":
		nave = "Motovedetta"
		pos = 4

	# sottrae una vita alla volta alla nave, quando la vita scende a zero stampa 'affondato'
	campo[-1][nave] -= 1
	if campo[-1][nave] == 0:
		print(color.colors.bg.red + "Nave affondata: " + nave + color.colors.reset)
		return pos, True  # boolean true se nave affondata
	else:
		return pos, False


# metodo che controlla se l'utente o il computer hanno vinto
def controlla_vittoria(campo):
	# ciclo nel campo e vedo se sono state affondate tutte le navi
	for i in range(10):
		for j in range(10):
			if campo[i][j] != -1 and campo[i][j] != '*' and campo[i][j] != 'X':
				return False
	return True


def main():
	input("Benvenuto sul campo di Battaglia, soldato. Il tuo obiettivo è affondare tutte le navi naviche!\nPremi INVIO per schierare la tua flotta...")

	# tipi di navi e relativa dimensione
	navi = {"Portaerei": 5,
	        "Corazzata": 4,
	        "Sottomarino": 3,
	        "Incrociatore": 3,
	        "Motovedetta": 2}

	# creiamo un classico campo da gioco di dimensioni 10x10
	campo = []
	for i in range(10):
		riga_campo = []
		for j in range(10):
			riga_campo.append(-1)  # -1 è il simbolo che rappresenta l'acqua
		campo.append(riga_campo)

	# creo i campi da gioco, sia del giocatore che del computer
	campo_giocatore = copy.deepcopy(campo)
	campo_computer = copy.deepcopy(campo)

	# aggiungo le navi come ultimi elementi nella matrice
	campo_giocatore.append(copy.deepcopy(navi))
	campo_computer.append(copy.deepcopy(navi))

	# posiziono le navi nel campo
	campo_giocatore = posiziona_navi_giocatore(campo_giocatore, navi)
	campo_computer = posiziona_navi_computer(campo_computer, navi)

	# inizia la partita
	while 1:
		# mossa del giocatore
		stampa_campo("c", campo_computer)
		campo_computer = mossa_giocatore(campo_computer)

		# controllo se il giocatore ha vinto la partita
		if campo_computer == "VITTORIA":
			print("Hai VINTO la battaglia!!! Complimenti, soldato.")
			quit()

		# stampa il campo attuale del computer
		stampa_campo("c", campo_computer)
		input("Per terminare il tuo turno premere INVIO\n")

		# mossa del computer
		campo_giocatore = mossa_computer(campo_giocatore)

		# controllo se il computer ha vinto la partita
		if campo_giocatore == "VITTORIA":
			print("Il computer ha VINTO! Dimettiti, soldato!")
			quit()

		# mostra il campo del giocatore
		stampa_campo("u", campo_giocatore)
		input("Per far terminare il turno del pc premere INVIO\n")


if __name__ == "__main__":
	main()
