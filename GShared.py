class GShared:
    def __init__(self,bits_to_index,global_history_size):
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.branch_table = [0 for i in range(self.size_of_branch_table)]  #Primer tabla
        self.global_history_size =global_history_size                      #Entrada de la historia global
        self.global_history_size2=2**self.global_history_size              #Tabla de 2^m bits.
        self.global_history = 0                                            #Se define un global history en 0.
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
        
        
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tG-Shared")
        print("\tEntradas en el Predictor:\t\t\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registro de historial global:\t\t\t"+str(self.global_history_size))

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        self.perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(self.perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")
#Función de predicción.
    def predict(self, PC):
        aux = int(PC) % self.size_of_branch_table 
        global_history = self.global_history % self.global_history_size2
        index = aux ^ global_history
        branch_table_entry = self.branch_table[index]
        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"
#Función de actualización.
    def update(self, PC, result, prediction):
        aux = int(PC) % self.size_of_branch_table #Indexo los s bits de entrada.
        global_history = self.global_history % self.global_history_size2 #Obtengo el módulo entre la historia global y la tabla de 2^m.
        index = aux ^ global_history              #Hago una o exclusiva para ver si tomo o no el salto. Este resultado queda en index.
        branch_table_entry = self.branch_table[index] #El resultado de index se pasa a esta tabla la cual se encargará de ir obteniendo los resultados.

        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
            
        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1

        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry

        else:
            updated_branch_table_entry = branch_table_entry + 1

        self.branch_table[index] = updated_branch_table_entry #Actualiza la tabla.

        #Máscara de para limitar la cantidad de bits. En esta caso se limita a 6bits.
       # self.global_history = self.global_history*2 & (self.global_history_size2-1) if result == "N" else self.global_history*2+1 & (self.global_history_size2-1)
        
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
