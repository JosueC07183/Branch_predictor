
class PShared:
    def __init__(self, bits_to_index, local_history_size):
        self.bits_to_index = bits_to_index                              #bimodal, bits de entrada.
        self.size_of_branch_table = 2**bits_to_index                     #bimodal
        self.local_history_size= local_history_size                     #bit de entrada
        self.size_of_local_history= 2**local_history_size               #tamaño de la tabla, 2^m
        self.branch_table = [0 for i in range(self.size_of_branch_table)] #Segunda tabla, tamaño de la tabla de la historia local. 
        self.branch_table_patrones=[0 for i in range(self.size_of_local_history)] #Tercer tabla.
        self.local_history =0
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
#Información a imprimir
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\t\t\tP-shared")
        print("\tEntradas en el History table:\t\t\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia local:\t\t\t"+str(self.local_history_size))
        print("\tEntradas en el pattern table:\t\t\t\t\t"+str(2**self.local_history_size))

#Esta función me permite mostrar los resultados.
    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")
    def predict(self, PC):
        index= int(PC) % self.size_of_branch_table #Esta es la primera tabla
        branch_table_pattern= self.branch_table[index]  #Aqui estoy tomando lo que esta saliendo de la primer tabla
        branch_table_entry = self.branch_table_patrones[branch_table_pattern]  #Aqui estoy tomando lo que esta saliendo de la segunda tabla.
        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"
    def update(self, PC, result, prediction):
        index= int(PC) % self.size_of_branch_table #Esta es la primera tabla
        branch_table_pattern= self.branch_table[index]  #Aqui estoy tomando lo que esta saliendo de la primer tabla
        branch_table_entry = self.branch_table_patrones[branch_table_pattern]  #
        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
            
        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1
            
        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry
            
        else:
            updated_branch_table_entry = branch_table_entry + 1
        self.branch_table_patrones[branch_table_pattern] = updated_branch_table_entry   #Actualizo la tercer tabla.
        
        #Update stats
        #En todos los casos se le hace un sll de un 1, pero cuando result == "T" se le suma a la segunda tabla.
        #Los demás casos es un 0, pero no hace falta ponerlo.
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
            self.branch_table[index]= self.branch_table[index] <<1 
            self.branch_table[index] += 1

        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
            self.branch_table[index]= self.branch_table[index] <<1
            self.branch_table[index] +=1

        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
            self.branch_table[index]= self.branch_table[index] <<1

        else:
            self.total_not_taken_pred_taken += 1
            self.branch_table[index]= self.branch_table[index] <<1

        self.total_predictions += 1
        #Aquí se limita la cantidad de bits y se evita que se salga del rango esperado.
        self.branch_table[index]=self.branch_table[index]%self.size_of_local_history
        
