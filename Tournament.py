from GShared import *        #Hacer este import permite usar las variables internas de este predictor.
from PShared import *       #Este import da la oportunidad de usar variables internas del predictor PShared.

class Tournament:
    def __init__(self, bits_to_index, global_history_size, local_history_size):  #Se traen las variables de los predictores GShared y PShared.
        self.bits_to_index = bits_to_index
        self.global_history_size = global_history_size        #Esta variable pertenece al GShared
        self.local_history_size = local_history_size          #Esta variable pertenece al PShared
        self.predictor_count = 0
        self.gs_global = GShared(bits_to_index,global_history_size) #Será necesaria para hacer el llamado y poder realizar la respectiva comparación con el PShared.
        self.ps_local = PShared(bits_to_index,local_history_size)   #Se accede a la tabla de historia local para hacer el llamado y comparar con el GShared.
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
#Se muestra la info del predictor.
    def print_info(self):
        print("Parámetros del predictor:")
        print("Tipo de predictor:")
        print("Sobre el predictor Global:")
        print("\tEntradas del predictor global:\t\t\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia global:\t\t\t\t\t"+str(self.global_history_size))
        print("Sobre el predictor Local:")
        print("\tEntradas en el History Table:\t\t\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia local:"+str(self.local_history_size))
        print("\tEntradas en el Pattern Table: "+ str(2**self.local_history_size))
   #Se imprimen las estadisticas y demás información del predictor. 
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
   #Se debe crear una función con un contador con el fin de saber que predictor se va a
   # usar, entonces según las condiciones del if el contador va a trabajar con base a esto.
   #Es decir, básicamente con esta nueva función lo que se hace es una comparación de
   #ambos predictores.
    def predict_and_update(self, PC, result):

        ps_local = self.ps_local.predict(PC)     #La variable ps_local se define como la tabla del PC.
        gs_global = self.gs_global.predict(PC)   #La variable gs_global se define como la tabla del PC.

#El siguiente condicional determinará que predictor es el que va a prevalecer.
#Previamente se mencionó un contador, entonces lo que va a-
#hacer este es determinar en que condiciones va a sumar o restar. Entonces se evalua si el 
#contador esta en ese array, la variable prediction es ahora ps_local, sino el gs_global.
        if self.predictor_count in [0,1]:    
            prediction = ps_local             
        else:
            prediction = gs_global
#A continuación se hace actualización dependiendo del resultado del predictor.
        self.ps_local.update(PC,result, ps_local)
        self.gs_global.update(PC,result, gs_global)
#En el siguiente bloque de código se evalua (por eso el símbolo ==) si la tabla del ps_local es igual a la variable
#result y si gs_global es diferente de result lo que va a pasar es que se comprueba si el contador es distinto de 0 (o sea-
# el salto no se toma) y de ser así, el contador va a restar 1.
        if ps_local == result and gs_global != result:
            if self.predictor_count !=0:
                self.predictor_count -= 1 
#Luego, si ps_local resultar ser distinto a result y gs_global igual que result se procede a
#ver si el contador es distinta a tomado (por eso un 3), de ser así, el contador suma una unidad.
        elif ps_local != result and gs_global == result:
            if self.predictor_count !=3:
                self.predictor_count += 1 

        #Update stats
        #Misma lógica usada en el bimodal.
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1