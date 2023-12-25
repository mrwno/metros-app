import folium, io, json, sys, math, random, os
import psycopg2
from folium.plugins import Draw, MousePosition, MeasureControl
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 600)
	
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
        self.rows = []

        self.webView = myWebView()
		
        controls_panel = QHBoxLayout()
        mysplit = QSplitter(Qt.Vertical)
        mysplit.addWidget(self.tableWidget)
        mysplit.addWidget(self.webView)

        main.layout().addLayout(controls_panel)
        main.layout().addWidget(mysplit)

        _label = QLabel('From: ', self)
        _label.setFixedSize(30,30)
        self.from_box = QComboBox() 
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        predefined_value = "Riquet"
        self.from_box.addItem(predefined_value)

        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)
        #Sert ??? mettre des valeurs pr???d???finies dans le From
        _label = QLabel('  To: ', self)
        _label.setFixedSize(20,20)
        self.to_box = QComboBox() 
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)
        #Sert ??? mettre des valeurs pr???d???finies dans le To
        predefined_value = "Châ?telet"
        self.to_box.addItem(predefined_value)

        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)

        _label = QLabel('Methode: ', self)
        _label.setFixedSize(60,60)
        self.meth_box = QComboBox() 
        self.meth_box.addItems( ['Metro', 'Tram', 'Bus', 'Walk', 'Train','Tout'] )
        self.meth_box.setCurrentIndex( 0 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.meth_box)
        
        _label = QLabel('Hops: ', self)
        _label.setFixedSize(30,30)
        self.hop_box = QComboBox() 
        self.hop_box.addItems( ['1', '2', '3', '4', '5'] )
        self.hop_box.setCurrentIndex( 0 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.hop_box)

        self.go_button = QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        controls_panel.addWidget(self.go_button)
           
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.button_Clear)
        controls_panel.addWidget(self.clear_button)

        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        controls_panel.addWidget(self.maptype_box)

           
        self.connect_DB()

        self.startingpoint = True
                   
        self.show()
        

    def connect_DB(self):
        self.conn = psycopg2.connect(database="l3info_61", user="l3info_61", host="10.11.11.22", password="L3INFO_61")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct name FROM nodes""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows : 
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))


    def table_Click(self):
        print("Row number double-clicked: ", self.tableWidget.currentRow())
        i = 0
        for col in self.rows[self.tableWidget.currentRow()] :
            print(f"{i} column value is: {col}")
            if type(col)=='decimal.Decimal':
                print(hello)

      
            i = i + 1
        

            
        

    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())
        self.valeur=str(self.meth_box.currentText()) #sert à? prendre le type de transport 

        self.rows = []
        self.rows2 = []
        self.rows_new=[]
        self.rows_new2=[]
        self.res = []
        self.res2=[]
        self.res3=[]
        self.res_combined = []
        route=[]
        if _hops >= 8 : 
            self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND B.to_stop_I = D.stop_I AND D.name = $${_tostation}$$""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()
            print(self.rows)
            self.res+=self.compare2(self.rows)
            
        if _hops >= 8 : #ATTENTION A REMPLACER 
            self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND B.to_stop_I = D.stop_I """)
            self.conn.commit()
            self.rows += self.cursor.fetchall()
            self.res7=self.compare(self.rows)
            for elementsss in self.res7:
                if self.res7.count(elementsss)>=2:
                    self.res7.remove(elementsss)
            print("Mon rows est",self.res7)
            for e in range(len(self.res7)):
                print("##############################################")
                fromi=self.res7[e][2]
                print("Mon from_station est",fromi)
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${fromi}$$ AND B.to_stop_I = D.stop_I AND D.name=$${_tostation}$$""")
                self.conn.commit()
                self.rows_new += self.cursor.fetchall()
                self.rows=self.rows_new

                self.res_new=self.compare(self.rows)

                print("Mon res3  est donc ",self.res_new)
    
            self.res_combined = []
            for ligne_res7 in self.res7:
                for ligne_res_new in self.res_new:
                    # Verifier si les criteres de fusion sont satisfaits
                    if (ligne_res7[2] == ligne_res_new[0]) and (ligne_res7[1] != ligne_res_new[1]) and (ligne_res_new[0] != ligne_res_new[2]):
                        # Fusionner les lignes en creant une nouvelle liste
                        nouvelle_ligne = ligne_res7 + ligne_res_new[1:]
                        # Ajouter la nouvelle ligne au tableau combine
                        self.res_combined.append(nouvelle_ligne)
            self.res += self.res_combined
        
        
        if _hops == 3  : #ATTENTION  ++++++++++++++++++++
            #je vais d abord m occuper du cote gauche
            if self.valeur=='Metro':
                print("Ma valeur est",self.valeur)
                self.rows=[]
                self.res_combined=[]
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND B.to_stop_I = D.stop_I """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                self.res7=self.compare(self.rows)
                for elementsss in self.res7:
                    if self.res7.count(elementsss)>=2:
                        self.res7.remove(elementsss)
                print("Mon cote gauche est ",self.res7)
                
                self.rows=[]
                #maintenant, je m occupe du cote droit
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND B.to_stop_I = D.stop_I AND D.name = $${_tostation}$$  """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                self.res8=self.compare(self.rows)
                for elementsss in self.res8:
                    if self.res8.count(elementsss)>=2:
                        self.res8.remove(elementsss)
                print("\n###########Mon cote droit est",self.res8)
                #je vais un lien entre les deux parties
                self.rows=[]
                for element in self.res7:
                    _from=element[2]
                    for element2 in self.res8:
                        _to=element2[0]
                        self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_from}$$ AND B.to_stop_I = D.stop_I AND D.name = $${_to}$$  """)
                        self.conn.commit()
                        self.rows= self.cursor.fetchall()
                        self.res9=self.compare(self.rows)
                    if len(self.res9) !=0:
                        print("Ma combinaison est",element,self.res9,element2)
                        
                        nouveau=(element[0],element[1])+(self.res9[0][0],self.res9[0][1])+element2
                        self.res_combined.append(nouveau)
                self.res=self.res_combined
########################################################################################################"            
            if self.valeur=='Bus':
                print("Ma valeur est",self.valeur)
                self.rows=[]
                self.res_combined=[]
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM bus as A, bus AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND B.to_stop_I = D.stop_I """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                self.res7=self.compare(self.rows)
                for elementsss in self.res7:
                    if self.res7.count(elementsss)>=2:
                        self.res7.remove(elementsss)
                print("Mon cote gauche est ",self.res7)
                
                self.rows=[]
                #maintenant, je m occupe du cote droit
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM bus as A, bus AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND B.to_stop_I = D.stop_I AND D.name = $${_tostation}$$  """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                self.res8=self.compare(self.rows)
                for elementsss in self.res8:
                    if self.res8.count(elementsss)>=2:
                        self.res8.remove(elementsss)
                print("\n###########Mon cote droit est",self.res8)
                #je vais un lien entre les deux parties
                self.rows=[]
                for element in self.res7:
                    _from=element[2]
                    for element2 in self.res8:
                        _to=element2[0]
                        self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM bus as A, bus AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_from}$$ AND B.to_stop_I = D.stop_I AND D.name = $${_to}$$  """)
                        self.conn.commit()
                        self.rows= self.cursor.fetchall()
                        self.res9=self.compare(self.rows)
                    if len(self.res9) !=0:
                        print("Ma combinaison est",element,self.res9,element2)
                        
                        nouveau=(element[0],element[1])+(self.res9[0][0],self.res9[0][1])+element2
                        self.res_combined.append(nouveau)
                self.res=self.res_combined
#############################################################################################################

            else:
                print("je n'ai rien")
        #print("##################################################################################")
        #print("Mon res final est ",self.res_new)"""
        
        #sert à? sé?parer les doublons
        self.res = [list(x) for x in set(tuple(x) for x in self.res_combined)]
        
        print("mon final est ", self.res)

        if len(self.res) == 0 : 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        numrows = len(self.res)
        numcols = (_hops * 2)+1
        self.tableWidget.setRowCount(numrows)
        self.tableWidget.setColumnCount(numcols)

        i = 0
        for row in self.res : 
            #print("Ma ligne est ",row)
            j = 0
            for colonne in row :
                #print("Ma colonne est",colonne)
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(colonne)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < numcols :
            header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
            j = j+1
        
        self.update()


   
    def compare(self,rows):
        #print("Mon res est",self.rows)
        #print("##################################################################################")
        self.rows2 = []
        self.rs = []
        self.res2=[]
        for i in range(len(self.rows)):
            #print("Je vais faire", len(self.rows))
            tuple=()
            for element in self.rows[i][1]:
                for elements in self.rows[i][3]:
                    if element == elements:
                        #print("mon element 1 est", element)
                        #print("mon element 2 est", elements)
                        for j in range(len(self.rows[-1])-1):
                            #print(j)
                            if (j != 1):
                                #print("je vais ajouter",self.rows[i][j])
                                tuple=tuple+(self.rows[i][j],)


                            else:
                                #print("je vais executer cette commande")
                                self.cursor.execute(""f" SELECT distinct A.route_name FROM paris_to as A WHERE A.route_i = $${element}$$ """)
                                self.conn.commit()
                                self.rows2 = self.cursor.fetchall()
                                tuple=tuple+(self.rows2[0][0],)
            if(len(tuple)>3 ):
                self.rs.append((tuple[0],tuple[1],tuple[2]))
                
            else:
                self.rs.append(tuple)

        for element in self.rs: 
            if element != () :
                self.res2.append(element)
        #print("Mon res2 est",self.res2[8][2])

        for element in self.res2:
            if self.res2.count(element)>=2:
                self.res2.remove(element)
        return self.res2

    def compare2(self,rows):
        self.rows2 = []
        self.rs = []
        for i in range(len(self.rows)):
            #print("Je vais faire", len(self.rows))
            for element in self.rows[i][1]:
                for elements in self.rows[i][3]:
                    if element == elements:
                        #print("mon element 1 est", element)
                        #print("mon element 2 est", elements)
                        for j in range(len(self.rows[-1])-1):
                            #print(j)
                            if (j != 1):
                                #print("je vais ajouter",self.rows[i][j])
                                self.rs.append(self.rows[i][j])

                            else:
                                #print("je vais executer cette commande")
                                self.cursor.execute(""f" SELECT distinct A.route_name FROM paris_to as A WHERE A.route_i = $${element}$$ """)
                                self.conn.commit()
                                self.rows2 += self.cursor.fetchall()
                                self.rs.append(self.rows2[0][0])

        #print("Mon res est",self.rs)
        return self.rs

    
    def egale(self,origin,finish):
        self.rows_egale=[]
        self.res_egale=[]
        self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM subway as A, subway AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${origin}$$ AND B.to_stop_I = D.stop_I AND D.name = $${finish}$$""")
        self.conn.commit()
        self.rows_egale += self.cursor.fetchall()
        #print(self.rows_egale)
        self.res_egale+=self.compare2(self.rows_egale)
        
        if(len(self.res_egale) == 0):
            return False
        return True
    
    
            
        
    def button_Clear(self):
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.update()


    def mouseClick(self, lat, lng):
        self.webView.addPoint(lat, lng)

        print(f"Clicked on: latitude {lat}, longitude {lng}")
        self.cursor.execute(""f" WITH mytable (distance, name2) AS (SELECT ( ABS((lat-{lat})*(lat-{lat})) + ABS((lon-{lng})*(lon-{lng})) ), name FROM nodes) SELECT name2 FROM mytable  WHERE distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
        self.conn.commit()
        rows = self.cursor.fetchall()
        #print('Closest STATION is: ', rows[0][0])
        if self.startingpoint :
            self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
        else :
            self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
        self.startingpoint = not self.startingpoint



class myWebView (QWebEngineView):
    def __init__(self):
        super().__init__()

        self.maptypes = ["OpenStreetMap", "Stamen Terrain", "stamentoner", "cartodbpositron"]
        self.setMap(0)


    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object


    def handleClick(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']

        window.mouseClick(lat, lng)


    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
        """
        L.polyline(
            [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                "color": "red",
                "opacity": 1.0,
                "weight": 4,
                "line_cap": "butt"
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2 )

        self.page().runJavaScript(js)


    def addMarker(self, lat, lng):
        js = Template(
        """
        L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def addPoint(self, lat, lng):
        js = Template(
        """
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": 'green',
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": 'green',
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def setMap (self, i):
        self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True)

        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)



class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        #print(msg)
        if 'coordinates' in msg:
            self.parent.handleClick(msg)


       
			
if __name__ == '__main__':
    sys.argv.append('--no-sandbox')
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
