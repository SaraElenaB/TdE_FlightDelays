import flet as ft
from markdown_it.rules_core.normalize import NULL_RE


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._aeroportoPartenza= None
        self._aeroportoArrivo= None

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def handleAnalisiAeroporti(self, e):

        nMinCompagnie = self._view._txtInMin.value
        if nMinCompagnie == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione! Inserire un numero minimo di compagnie", color="red"))
            self._view.update_page()
            return

        try:
            min = int(nMinCompagnie)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione! Inserire un valore numerico", color="red"))
            self._view.update_page()
            return

        if min < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Inserire un valore positivo", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(min)

        #solo dopo che creo il grafo posso riempire i due dd
        allNodes= self._model.getAllNodes()
        self._fillDD(allNodes)

        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato! \nNum di nodi:  {numNodes} \nNum di archi: {numEdges} "))
        self._view.update_page()
        return

    def _fillDD(self, nodes):

        for node in nodes:
            self._view._ddAeroportoP.options.append( ft.dropdown.Option( key=node.IATA_CODE,
                                                                         data=node,
                                                                         on_click= self._choiceDDPartenza))

            self._view._ddAeroportoA.options.append(ft.dropdown.Option(key=node.IATA_CODE,
                                                                       data=node,
                                                                       on_click=self._choiceDDArrivo))

    def _choiceDDPartenza(self, e):
        self._aeroportoPartenza = e.control.data
        print(f"_aeroportoPartenza called: {self._aeroportoPartenza} ")

    def _choiceDDArrivo(self, e):
        self._aeroportoArrivo = e.control.data
        print(f"_aeroportoArrivo called: {self._aeroportoArrivo} ")

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def handleConnessiAeroporti(self, e):

        if self._aeroportoPartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un aeroporto", color="red"))
            self._view.update_page()
            return

        neighborsTuple = self._model.getSortedNeighbors(self._aeroportoPartenza)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Dato {self._aeroportoPartenza} i suoi vicini sono i seguenti: "))
        for v in neighborsTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso:{v[1]}"))

        self._view.update_page()

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def handleEsistePercorso(self, e):

        if self._aeroportoPartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un aeroporto", color="red"))
            return

        if self._aeroportoArrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un aeroporto", color="red"))
            return

        path = self._model.getPath(self._aeroportoPartenza, self._aeroportoArrivo)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Non è stato trovato nessun percorso", color="red"))
            return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Cammino tra {self._aeroportoPartenza} e {self._aeroportoArrivo} trovato. \nDi seguito i nodi del cammino:"))

            for p in path:
                self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def handleCercaItinerario(self, e):
        pass

    #-----------------------------------------------------------------------------------------------------------------------------------------