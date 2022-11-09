from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import *
from datetime import datetime
import sys
import os

import CategoriseerVenster
import TransactieData

# om te compileren tot standalone app, run het volgende commando in de terminal:
# python -m PyInstaller gui.py -n "Kostenoverzicht" --windowed --onefile
def main():
  app = QApplication(sys.argv)
  window = MainWindow()

  window.show()
  sys.exit(app.exec_())

   
class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.transactieData = TransactieData.TransactieData()

    self.setWindowTitle('Kasboekje')
    
    self.triodosLaadKnop = QPushButton('importeer Triodos', self)
    self.triodosLaadKnop.clicked.connect(self.laadTriodos)
    self.triodosLaadKnop.resize(110,25)

    self.categoriseerTransactiesKnop = QPushButton('categoriseer auto', self)
    self.categoriseerTransactiesKnop.clicked.connect(self.categoriseerTransactiesAutomatisch)
    self.categoriseerTransactiesKnop.resize(110,25)

    self.categoriseerTransactiesHandmatigKnop = QPushButton('categoriseer zelf', self)
    self.categoriseerTransactiesHandmatigKnop.clicked.connect(self.categoriseerTransactiesHandmatig)
    self.categoriseerTransactiesHandmatigKnop.resize(110,25)

    self.transactieOverzicht = QTextEdit(self)
    self.transactieOverzicht.setFontFamily('consolas')
    self.transactieOverzicht.setText('')
    self.transactieOverzicht.setReadOnly(True)
    self.transactieOverzicht.resize(580,250)
    self.transactieOverzicht.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    self.transactiesOpslaanKnop = QPushButton('transacties opslaan', self)
    self.transactiesOpslaanKnop.clicked.connect(self.transactiesOpslaan)
    self.transactiesOpslaanKnop.resize(110,25)
    self.csvLadenKnop = QPushButton('transacties laden', self)
    self.csvLadenKnop.clicked.connect(self.transactiesLaden)
    self.csvLadenKnop.resize(110,25)

    self.transactieOverzichtCategorie = QComboBox(self)
    self.transactieOverzichtCategorie.addItem('alles')
    self.transactieOverzichtCategorie.addItems(self.transactieData.categorieOverzicht())
    self.transactieOverzichtCategorie.activated.connect(self.updateTransactieOverzicht)
    self.transactieOverzichtCategorie.resize(110, 25)

    self.inTotaalLabel = QLabel(self)
    self.inTotaalLabel.setText('totaal in:')
    self.inTotaalLabel.resize(60,25)
    self.inTotaalBedrag = QLineEdit(self)
    self.inTotaalBedrag.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.inTotaalBedrag.setReadOnly(True)
    self.inTotaalBedrag.resize(70,25)

    self.uitTotaalLabel = QLabel(self)
    self.uitTotaalLabel.setText('totaal uit:')
    self.uitTotaalLabel.resize(60,25)
    self.uitTotaalBedrag = QLineEdit(self)
    self.uitTotaalBedrag.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.uitTotaalBedrag.setReadOnly(True)
    self.uitTotaalBedrag.resize(70,25)

    self.totaalLabel = QLabel(self)
    self.totaalLabel.setText('totaal:')
    self.totaalLabel.resize(60,25)
    self.totaalBedrag = QLineEdit(self)
    self.totaalBedrag.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.totaalBedrag.setReadOnly(True)
    self.totaalBedrag.resize(70,25)

    self.aantalLabel = QLabel(self)
    self.aantalLabel.setText('aantal:')
    self.aantalLabel.resize(60,25)
    self.aantal = QLineEdit(self)
    self.aantal.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.aantal.setReadOnly(True)
    self.aantal.resize(70,25)

    self.startDatumLabel = QLabel(self)
    self.startDatumLabel.setText('startdatum:')
    self.startDatumLabel.resize(60,25)
    self.startDatumSelectie = QDateEdit(self)
    self.startDatumSelectie.resize(80,25)
    self.startDatumSelectie.editingFinished.connect(self.updateTransactieOverzicht)

    self.eindDatumLabel = QLabel(self)
    self.eindDatumLabel.setText('einddatum:')
    self.eindDatumLabel.resize(60,25)
    self.eindDatumSelectie = QDateEdit(self)
    self.eindDatumSelectie.resize(80,25)
    self.eindDatumSelectie.editingFinished.connect(self.updateTransactieOverzicht)

    self.zoektermOverzichtLabel = QLabel(self)
    self.zoektermOverzichtLabel.setText('zoektermen')
    self.zoektermOverzichtLabel.resize(110, 25)

    self.zoektermOverzicht = QTextEdit(self)
    self.zoektermOverzicht.setFontFamily('consolas')
    self.zoektermOverzicht.setText(self.transactieData.zoektermOverzicht())
    self.zoektermOverzicht.setReadOnly(True)
    self.zoektermOverzicht.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    self.voegCategorieToeKnop = QPushButton('voeg categorie toe', self)
    self.voegCategorieToeKnop.clicked.connect(self.voegCategorieToe)
    self.voegCategorieToeKnop.resize(110,25)

    self.voegZoektermToeKnop = QPushButton('voeg zoekterm toe', self)
    self.voegZoektermToeKnop.clicked.connect(self.voegZoektermToe)
    self.voegZoektermToeKnop.resize(110,25)

    self.verwijderZoektermKnop = QPushButton('verwijder zoekterm', self)
    self.verwijderZoektermKnop.clicked.connect(self.verwijderZoekterm)
    self.verwijderZoektermKnop.resize(110,25)

    self.opslaanZoektermKnop = QPushButton('zoektermen opslaan', self)
    self.opslaanZoektermKnop.clicked.connect(self.zoektermenOpslaan)
    self.opslaanZoektermKnop.resize(110, 25)

    self.ladenZoektermKnop = QPushButton('zoektermen laden', self)
    self.ladenZoektermKnop.clicked.connect(self.zoektermenLaden)
    self.ladenZoektermKnop.resize(110, 25)

    self.resize(1000, 600)


  def resizeEvent(self, event):
    w = max(self.width(), 1000)
    h = max(self.height(), 600)

    self.transactieOverzichtCategorie.move(10, 10)
    self.categoriseerTransactiesKnop.move(130,10)
    self.categoriseerTransactiesHandmatigKnop.move(250,10)

    self.transactieOverzicht.move(10,45)
    self.transactieOverzicht.resize(2*w//3-30, h-160)

    self.triodosLaadKnop.move(10, h-100)
    self.transactiesOpslaanKnop.move(10, h-70)
    self.csvLadenKnop.move(10, h-40)

    self.inTotaalLabel.move(160, h-100)
    self.uitTotaalLabel.move(160, h-70)
    self.inTotaalBedrag.move(220, h-100)
    self.uitTotaalBedrag.move(220, h-70)

    self.totaalLabel.move(330, h-100)
    self.aantalLabel.move(330, h-70)
    self.totaalBedrag.move(380, h-100)
    self.aantal.move(380, h-70)

    self.startDatumLabel.move(490, h-100)
    self.eindDatumLabel.move(490, h-70)
    self.startDatumSelectie.move(560, h-100)
    self.eindDatumSelectie.move(560, h-70)

    self.zoektermOverzichtLabel.move(2*w//3,25)
    self.zoektermOverzicht.resize(w//3-10, h//3)
    self.zoektermOverzicht.move(2*w//3, 45)

    self.voegCategorieToeKnop.move(2*w//3, h//3+60)
    self.voegZoektermToeKnop.move(2*w//3, h//3+90)
    self.opslaanZoektermKnop.move(2*w//3, h//3+120)
    self.verwijderZoektermKnop.move(2*w//3+120, h//3+90)
    self.ladenZoektermKnop.move(2*w//3+120, h//3+120)


  def laadTriodos(self):
    fname = QFileDialog.getOpenFileName(self, 'Open Triodos transactieoverzicht', 'C:\\Users\\Xander\\Downloads', 'excel bestand (*.xlsx)')
    if not os.path.exists(fname[0]):
      return
    self.transactieData.verwijderAlleTransacties()
    self.transactieData.transactiesImporterenTriodos(fname[0])
    self.updateDatumSelectie()
    self.updateTransactieOverzicht()

  def transactiesOpslaan(self):
    fname = QFileDialog.getSaveFileName(self, 'Transacties opslaan als', 'D:\\', 'csv bestand (*.csv)')
    if fname[0]:
      self.transactieData.transactiesExporterenCsv(fname[0])

  def transactiesLaden(self):
    fname = QFileDialog.getOpenFileName(self, 'Open transacties', 'D:\\', 'csv bestand (*.csv)')
    if not os.path.exists(fname[0]):
      return
    self.transactieData.verwijderAlleTransacties()
    self.transactieData.transactiesImporterenCsv(fname[0])
    self.updateDatumSelectie() 
    self.updateTransactieCategorien()
    self.updateZoektermOverzicht()
    self.updateTransactieOverzicht()

  def categoriseerTransactiesAutomatisch(self):    
    self.transactieData.categoriseerTransactiesMetZoektermen()
    self.updateTransactieOverzicht()

  def categoriseerTransactiesHandmatig(self):
    d = CategoriseerVenster.CategoriseerVenster()
    d.setTransactieData(self.transactieData)

    result = d.exec_()
    if result==1:
      self.transactieData = d.transactieData
      self.updateZoektermOverzicht()
      self.updateTransactieCategorien()
      self.updateTransactieOverzicht()

  def voegCategorieToe(self):
    d = QDialog()

    naam = QLineEdit(d)
    naam.move(10,10)
    naam.resize(110,25)

    okKnop = QPushButton("ok",d)
    okKnop.move(10,45)
    okKnop.clicked.connect(d.accept)

    result = d.exec_()
    if result==1:
      categorie = naam.text()
      self.transactieData.voegCategorieToe(categorie)
      self.updateZoektermOverzicht()
      self.transactieOverzichtCategorie.addItem(categorie)

  def voegZoektermToe(self):
    d = QDialog()

    categorie = QComboBox(d)
    categorieen = self.transactieData.categorieOverzicht()
    beschermdeCategorien = self.transactieData.beschermdeCategorieLijst()
    categorie.addItems(list(set(categorieen) - set(beschermdeCategorien)))
    categorie.resize(110, 25)
    categorie.move(10, 10)

    zoekterm = QLineEdit(d)
    zoekterm.move(10,45)
    zoekterm.resize(110,25)

    okKnop = QPushButton("ok",d)
    okKnop.move(10,80)
    okKnop.clicked.connect(d.accept)
    result = d.exec_()

    if result==1:
      categorie = categorie.currentText()
      zoekterm = zoekterm.text()
      self.transactieData.voegZoektermToe(zoekterm, categorie)
      self.updateZoektermOverzicht()

  def verwijderZoekterm(self):
    d = QDialog()

    categorie = QComboBox(d)
    categorie.addItems(self.transactieData.categorieOverzicht())
    categorie.resize(110, 25)
    categorie.move(10, 10)

    zoekterm = QLineEdit(d)
    zoekterm.move(10,45)
    zoekterm.resize(110,25)

    okKnop = QPushButton("verwijder",d)
    okKnop.move(10,80)
    okKnop.clicked.connect(d.accept)

    result = d.exec_()
    if result==1:
      categorie = categorie.currentText()
      zoekterm = zoekterm.text()
      self.transactieData.verwijderZoekterm(zoekterm, categorie)
      self.updateZoektermOverzicht()

  def zoektermenOpslaan(self):
    fname = QFileDialog.getSaveFileName(self, 'Zoektermen opslaan als', 'D:\\', 'json bestand (*.json)')
    if fname[0]:
      self.transactieData.zoektermenOpslaan(fname[0])

  def zoektermenLaden(self):
    fname = QFileDialog.getOpenFileName(self, 'Open zoektermen', 'D:\\', 'json bestand (*.json)')
    if os.path.exists(fname[0]):
      self.transactieData.zoektermenLaden(fname[0])
    
    self.updateZoektermOverzicht()
    self.updateTransactieCategorien()
    self.updateTransactieOverzicht()

  def updateTransactieOverzicht(self):
    d=self.startDatumSelectie.date()
    startDatum = datetime(d.year(), d.month(), d.day())
    d=self.eindDatumSelectie.date()
    eindDatum = datetime(d.year(), d.month(), d.day())
    categorie = self.transactieOverzichtCategorie.currentText()
    self.transactieOverzicht.setText(self.transactieData.transactieOverzicht(categorie, startDatum=startDatum, eindDatum=eindDatum))

    totaal, inTotaal, uitTotaal, aantal = self.transactieData.berekenTotalen(categorie, startDatum, eindDatum)
    self.inTotaalBedrag.setText(f'{inTotaal:.2f}')
    self.uitTotaalBedrag.setText(f'{uitTotaal:.2f}')
    self.totaalBedrag.setText(f'{totaal:.2f}')
    self.aantal.setText(f'{aantal}')

  def updateZoektermOverzicht(self):
    self.zoektermOverzicht.setText(self.transactieData.zoektermOverzicht())

  def updateTransactieCategorien(self):
    self.transactieOverzichtCategorie.clear()
    self.transactieOverzichtCategorie.addItem('alles')
    self.transactieOverzichtCategorie.addItems(self.transactieData.categorieOverzicht())

  def updateDatumSelectie(self):
    firstDate, lastDate = self.transactieData.datumRange()
    self.startDatumSelectie.setDate(QDate(firstDate.year, firstDate.month, firstDate.day))
    self.eindDatumSelectie.setDate(QDate(lastDate.year, lastDate.month, lastDate.day))

if __name__ == "__main__":
  main()