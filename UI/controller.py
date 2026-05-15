import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        lista = self._model.getAnni()
        lista.sort()
        for element in lista:
            opzione = ft.dropdown.Option(f"{element}")
            self._view.ddyear.options.append(opzione)
        self._view.update_page()

    def fillShape(self,e, anno):
        lista = self._model.getForme(anno)
        for element in lista:
            opzione = ft.dropdown.Option(f"{element}")
            self._view.ddshape.options.append(opzione)
        self._view.btn_graph.disabled=False
        self._view.update_page()

    def handle_graph(self, e, forma, anno):
        self._view.txt_result.controls.clear()
        if forma == None or anno == None:
            stringa = "Non  hai selezionato dei campi coerenti"
            self._view.txt_result.controls.append(ft.Text(f"{stringa}", color="red"))
            self._view.update_page()
            return
        self._model.creaGrafo(forma, anno)
        titolo, stringa1 = self._model.output()
        stringa = ft.Text(titolo)
        self._view.txt_result.controls.append(stringa)
        stringa = ft.Text(stringa1)
        self._view.txt_result.controls.append(stringa)
        self._view.btn_path.disabled=False
        self._view.update_page()


    def handle_path(self, e):
        tes1, tes2 = self._model.ricorsione()
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"{tes1}"))
        self._view.txtOut2.controls.append(ft.Text(f"{tes2}"))
        self._view.update_page()
