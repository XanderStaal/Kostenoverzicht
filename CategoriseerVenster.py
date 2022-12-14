from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CategoriseerVenster(QDialog):
  def __init__(self):
    super(CategoriseerVenster, self).__init__()
    
    self.setWindowTitle('Categoriseren')
    self.resize(1500, 600)
    self.transactieData = None
    self.setWindowFlag(Qt.WindowMaximizeButtonHint)

    self.transactieLijst1 = QListWidget(self)
    self.transactieLijst1.setFont(QFont('consolas', 8))
    self.transactieLijst1.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    self.transactieLijst1Categorie = QComboBox(self)
    self.transactieLijst1Categorie.activated.connect(self.updateTransactieLijst1)
    self.transactieLijst1Categorie.resize(110, 25)

    self.transactieLijst2 = QListWidget(self)
    self.transactieLijst2.setFont(QFont('consolas', 8))
    self.transactieLijst2.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    self.transactieLijst2Categorie = QComboBox(self)
    self.transactieLijst2Categorie.activated.connect(self.updateTransactieLijst2)
    self.transactieLijst2Categorie.resize(110, 25)

    self.transactieLijstSorteerVolgorde = QComboBox(self)
    self.transactieLijstSorteerVolgorde.addItems(['datum ↑', 'datum ↓', 'bedrag ↑', 'bedrag ↓'])
    self.transactieLijstSorteerVolgorde.activated.connect(self.updateTransactieLijsten)
    self.transactieLijstSorteerVolgorde.resize(110, 25)

    self.transactieLijstSorteerVolgorde.resize(110, 25)
    self.verplaatsLRKnop = QPushButton('--->', self)
    self.verplaatsLRKnop.resize(110, 25)
    self.verplaatsLRKnop.clicked.connect(self.verplaatsLR)

    self.verplaatsRLKnop = QPushButton('<---', self)
    self.verplaatsRLKnop.resize(110, 25)
    self.verplaatsRLKnop.clicked.connect(self.verplaatsRL)

    self.categorieToevoegenKnop = QPushButton('Categorie toevoegen', self)
    self.categorieToevoegenKnop.resize(110, 25)
    self.categorieToevoegenKnop.clicked.connect(self.voegCategorieToe)

    self.OKknop = QPushButton('OK', self)
    self.OKknop.resize(110, 25)
    self.OKknop.clicked.connect(self.accept)

  def resizeEvent(self, event):
    w = max(self.width(), 1000)
    h = max(self.height(), 600)

    self.transactieLijst1.resize(w//2-100, h-80)
    self.transactieLijst1.move(10,60)
    self.transactieLijst2.resize(w//2-100, h-80)
    self.transactieLijst2.move(w//2+90,60)

    self.transactieLijst1Categorie.move(10, 10)
    self.transactieLijst2Categorie.move(w//2+90, 10)

    self.transactieLijstSorteerVolgorde.move(w//2-55, 10)

    self.verplaatsLRKnop.move(w//2-55, h//2-20)
    self.verplaatsRLKnop.move(w//2-55, h//2+20)

    self.OKknop.move(w//2-55, h-40)
    self.categorieToevoegenKnop.move(w//2-55, h//2-60)

  def setTransactieData(self, transactieData):
    self.transactieData = transactieData
    self.updateCategorieComboBoxen()
    self.updateTransactieLijst1()
    self.updateTransactieLijst2()

  def updateTransactieLijsten(self):
    self.updateTransactieLijst1()
    self.updateTransactieLijst2()

  def updateTransactieLijst1(self):
    sorteerMethode = self.transactieLijstSorteerVolgorde.currentText()
    sorteerHeader = sorteerMethode[:-2]
    sorteerVolgorde = True if sorteerMethode[-1] =='↑' else False

    headers = ['datum', 'bedrag', 'tegenrekening', 'omschrijving']
    categorie = self.transactieLijst1Categorie.currentText()
    self.transactieLijst1.clear()
    self.transactieLijst1.addItems(self.transactieData.transactieLijst(categorie, headers, sorteerHeader=sorteerHeader, rev=sorteerVolgorde)[2:])

  def updateTransactieLijst2(self):
    sorteerMethode = self.transactieLijstSorteerVolgorde.currentText()
    sorteerHeader = sorteerMethode[:-2]
    sorteerVolgorde = True if sorteerMethode[-1] =='↑' else False

    headers = ['datum', 'bedrag', 'tegenrekening', 'omschrijving']
    categorie = self.transactieLijst2Categorie.currentText()
    self.transactieLijst2.clear()
    self.transactieLijst2.addItems(self.transactieData.transactieLijst(categorie, headers, sorteerHeader=sorteerHeader, rev=sorteerVolgorde)[2:])

  def updateCategorieComboBoxen(self):
    categorie1 = self.transactieLijst1Categorie.currentText()
    categorie2 = self.transactieLijst2Categorie.currentText()
    categorieLijst = self.transactieData.categorieOverzicht()
    
    self.transactieLijst1Categorie.clear()
    self.transactieLijst1Categorie.addItems(categorieLijst)
    if categorie1 in categorieLijst:
      self.transactieLijst1Categorie.setCurrentIndex(categorieLijst.index(categorie1))

    self.transactieLijst2Categorie.clear()
    self.transactieLijst2Categorie.addItems(categorieLijst)
    if categorie1 in categorieLijst:
      self.transactieLijst2Categorie.setCurrentIndex(categorieLijst.index(categorie2))

  def verplaatsLR(self):
    indexen = sorted([x.row() for x in self.transactieLijst1.selectedIndexes()], reverse=True)
    categorieL = self.transactieLijst1Categorie.currentText()
    categorieR = self.transactieLijst2Categorie.currentText()
    for i in indexen:
      sorteerMethode = self.transactieLijstSorteerVolgorde.currentText()
      sorteerHeader = sorteerMethode[:-2]
      sorteerVolgorde = True if sorteerMethode[-1] =='↑' else False
      self.transactieData.sorteerTransacties(categorieL, sorteerHeader, sorteerVolgorde)
      self.transactieData.data[categorieR]['transacties'].append(self.transactieData.data[categorieL]['transacties'].pop(i))

    self.transactieData.sorteerTransacties()
    self.updateTransactieLijsten()

  def verplaatsRL(self):
    indexen = sorted([x.row() for x in self.transactieLijst2.selectedIndexes()], reverse=True)
    categorieL = self.transactieLijst1Categorie.currentText()
    categorieR = self.transactieLijst2Categorie.currentText()
    for i in indexen:
      sorteerMethode = self.transactieLijstSorteerVolgorde.currentText()
      sorteerHeader = sorteerMethode[:-2]
      sorteerVolgorde = True if sorteerMethode[-1] =='↑' else False
      self.transactieData.sorteerTransacties(categorieR, sorteerHeader, sorteerVolgorde)
      self.transactieData.data[categorieL]['transacties'].append(self.transactieData.data[categorieR]['transacties'].pop(i))

    self.transactieData.sorteerTransacties()
    self.updateTransactieLijsten()

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
      self.updateCategorieComboBoxen()
