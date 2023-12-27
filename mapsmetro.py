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
        _label.setFixedSize(15,15)
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
        _label.setFixedSize(15,15)
        self.to_box = QComboBox() 
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)
        #Sert ??? mettre des valeurs pr???d???finies dans le To
        predefined_value = "Châtelet"
        self.to_box.addItem(predefined_value)

        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)
        
        _label = QLabel('Méthode: ', self)
        _label.setFixedSize(60,60)
        self.meth_box = QComboBox() 
        self.meth_box.addItems( ['subway', 'tram', 'bus', 'walk', 'rail','combined'] )
        self.meth_box.setCurrentIndex( 0 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.meth_box)

        _label = QLabel('Hops: ', self)
        _label.setFixedSize(20,20)
        self.hop_box = QComboBox() 
        self.hop_box.addItems( ['1', '2', '3'] )
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
        j = 0
        self.coord = []
        for col in self.res[self.tableWidget.currentRow()] :
            print(f"{i} column value is: {col}")
            if (i%2 == 0):
                self.cursor.execute(""f" SELECT lat, lon FROM nodes WHERE nodes.name = $${col}$$""")
                self.conn.commit()
                self.coord += self.cursor.fetchall()
            i = i + 1
        print(self.coord)
        for j in self.coord:
            self.webView.addMarker(j[0], j[1])
            if j != self.coord[0]:
                self.webView.addSegment(lat, lon, j[0], j[1])
                lat = j[0]
                lon = j[1]
            else:
                lat = j[0]
                lon = j[1]
                self.webView.addSegment(lat, lon, self.coord[1][0], self.coord[1][1])

        

    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())
        _meth = str(self.meth_box.currentText())

        self.rows = []
        self.rows2 = []
        self.rows_new=[]
        self.res = []
        self.res2=[]
        self.res3=[]
        route=[]
        if _meth == 'walk':
            if _hops >= 1 : 
                self.cursor.execute(""f" SELECT distinct C.name, A.d_walk, D.name FROM {_meth} AS A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND A.to_stop_I = D.stop_I AND D.name = $${_tostation}$$ GROUP BY C.name, A.d_walk, D.name HAVING A.d_walk <= ALL(SELECT distinct  A.d_walk FROM {_meth} AS A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND A.to_stop_I = D.stop_I AND D.name = $${_tostation}$$)""")
                self.conn.commit()
                self.res += self.cursor.fetchall()
                
            if _hops >= 2 :
                self.cursor.execute(""f" With fromstation(from_name, to_name, dist) AS (SELECT distinct C.name, D.name, A.d_walk FROM {_meth} as A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND A.to_stop_I = D.stop_I), tostation(from_name2,to_name2, dist2) AS (SELECT distinct C.name, D.name, A.d_walk FROM {_meth} as A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND D.name = $${_tostation}$$ AND A.to_stop_I = D.stop_I) SELECT E.from_name, dist, E.from_name2, dist2, E.to_name2 FROM (fromstation INNER JOIN tostation ON (fromstation.to_name = tostation.from_name2)) AS E WHERE from_name != to_name AND to_name != to_name2 GROUP BY from_name, dist, from_name2 ,dist2, to_name2 HAVING (dist + dist2) <= ALL(SELECT (dist + dist2) AS distance FROM (fromstation INNER JOIN tostation ON (fromstation.to_name = tostation.from_name2)) AS F WHERE from_name != to_name AND to_name != to_name2)""")
                self.res += self.cursor.fetchall()
                
            if _hops >= 3 :
                self.cursor.execute(""f" With fromstation(from_name, to_name, dist) AS (SELECT distinct C.name, D.name, A.d_walk  FROM {_meth} as A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND A.to_stop_I = D.stop_I), tostation(from_name2,to_name2, dist2) AS (SELECT distinct C.name, D.name, A.d_walk FROM {_meth} as A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND D.name = $${_tostation}$$ AND A.to_stop_I = D.stop_I), midstation(from_name3,to_name3, dist3) AS (SELECT distinct C.name, D.name, A.d_walk FROM {_meth} as A, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND A.to_stop_I = D.stop_I) SELECT F.from_name, F.dist, F.from_name3, F.dist3, F.to_name3, F.dist2, F.to_name2 FROM ((fromstation INNER JOIN midstation ON (fromstation.to_name = midstation.from_name3)) INNER JOIN tostation ON (to_name3 = tostation.from_name2)) AS F WHERE  from_name != from_name3 AND from_name3 != to_name3 AND to_name3 != to_name2 GROUP BY from_name, dist, from_name3 ,dist3, to_name3, dist2, to_name2 HAVING (dist + dist2 + dist3) <= ALL(SELECT (dist + dist2 + dist3) AS distance FROM ((fromstation INNER JOIN midstation ON (fromstation.to_name = midstation.from_name3)) INNER JOIN tostation ON (to_name3 = tostation.from_name2)) AS G WHERE from_name != from_name3 AND from_name3 != to_name3 AND to_name3 != to_name2) """)
                self.conn.commit()
                self.res += self.cursor.fetchall()

        if _meth != "walk":    
            if _hops >= 1 : 
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id, A.from_stop_i, B.to_stop_I FROM {_meth} as A, {_meth} AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND B.to_stop_I = D.stop_I AND D.name = $${_tostation}$$""")
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                #print(self.rows)
                self.res+=self.compare(self.rows)
                
            if _hops >= 2 :
                self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM {_meth} as A, {_meth} AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${_fromstation}$$ AND B.to_stop_I = D.stop_I """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                self.res7=self.compare(self.rows)
                for elementsss in self.res7:
                    if self.res7.count(elementsss)>=2:
                        self.res7.remove(elementsss)
                #print("Mon rows est",self.res7)
                for e in range(len(self.res7)):
                    #print("##############################################")
                    fromi=self.res7[e][2]
                    #print("Mon from_station est",fromi)
                    self.cursor.execute(""f" SELECT distinct C.name, A.bus_id, D.name, B.bus_id FROM {_meth} as A, {_meth} AS B, nodes AS C, nodes AS D WHERE A.from_stop_I = C.stop_I AND C.name = $${fromi}$$ AND B.to_stop_I = D.stop_I AND D.name=$${_tostation}$$""")
                    self.conn.commit()
                    self.rows_new += self.cursor.fetchall()
                    self.rows=self.rows_new
    
                    self.res_new=self.compare(self.rows)
    
                    #print("Mon res3  est donc ",self.res_new)
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
    
            #print("##################################################################################")
            #print("Mon res final est ",self.res_new)"""
        
        self.res = [list(x) for x in set(tuple(x) for x in self.res)]

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
            j = 0
            for colonne in row :
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


