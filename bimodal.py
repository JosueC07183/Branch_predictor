#Aqui es donde tengo que crear mis predictores.
class bimodal:
    def __init__(self, bits_to_index):
        self.bits_to_index = bits_to_index   #ie: 30 86629576
        self.size_of_branch_table = 2**bits_to_index
        self.branch_table = [0 for i in range(self.size_of_branch_table)]
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

#Aqui se imprime la info general
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tBimodal")
        print("\tEntradas en el Predictor:\t\t\t\t\t"+str(2**self.bits_to_index))    #Aqui se muestra la cantidad de entradas del predicto, es decir, 256. 

#Ahora los resultados
    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions)) #La cantidad de elementos en la primer columna.
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
#Esto es la suma de los saltos tomados y no tomados. Luego, se divide entre el total de branches, es decir, los 16M.
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions  
#Se toma el resultado final y se pone a 3 cifras significativas.
        formatted_perc = "{:.3f}".format(perc_correct)
#Se imprime el resultado final.
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

#Esta es la que hay que modificar. Agregar una tabla más etc.
    def predict(self, PC):
        index = int(PC) % self.size_of_branch_table
        branch_table_entry = self.branch_table[index]
        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"
#Aqui también.
    def update(self, PC, result, prediction):
        index = int(PC) % self.size_of_branch_table
        branch_table_entry = self.branch_table[index]

#Update entry accordingly
#Aqui el cero es: STRONGLY_NOT_TAKEN o NOT_TAKEN .
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry

        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1

#Aqui el 3 es STRONGLY_TAKEN.
        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry

        else:
            updated_branch_table_entry = branch_table_entry + 1

        self.branch_table[index] = updated_branch_table_entry

        #Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
