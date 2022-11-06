from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

class CategoriseerVenster(QDialog):
  def __init__(self):
    super(CategoriseerVenster, self).__init__()
    nx = 1500
    ny = 600
    self.resize(nx, ny)
    self.transactieData = None

    self.transactieLijst1 = QListWidget(self)
    self.transactieLijst1.setFont(QFont('consolas'))
    self.transactieLijst1.resize(nx//2-100, ny-80)
    self.transactieLijst1.move(10,60)
    self.transactieLijst1.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    self.transactieLijst1Categorie = QComboBox(self)
    self.transactieLijst1Categorie.activated.connect(self.updateTransactieLijsten)
    self.transactieLijst1Categorie.resize(110, 25)
    self.transactieLijst1Categorie.move(10, 10)

    self.transactieLijst2 = QListWidget(self)
    self.transactieLijst2.setFont(QFont('consolas'))
    self.transactieLijst2.resize(nx//2-100, ny-80)
    self.transactieLijst2.move(nx//2+90,60)
    self.transactieLijst2.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    self.transactieLijst2Categorie = QComboBox(self)
    self.transactieLijst2Categorie.activated.connect(self.updateTransactieLijsten)
    self.transactieLijst2Categorie.resize(110, 25)
    self.transactieLijst2Categorie.move(nx//2+90, 10)

    self.verplaatsLRKnop = QPushButton('--->', self)
    self.verplaatsLRKnop.resize(110, 25)
    self.verplaatsLRKnop.move(nx//2-55, ny//2-20)
    self.verplaatsLRKnop.clicked.connect(self.verplaatsLR)

    self.verplaatsRLKnop = QPushButton('<---', self)
    self.verplaatsRLKnop.resize(110, 25)
    self.verplaatsRLKnop.move(nx//2-55, ny//2+20)
    self.verplaatsRLKnop.clicked.connect(self.verplaatsRL)

    self.CategorieToevoegenKnop = QPushButton('Categorie toevoegen', self)
    self.CategorieToevoegenKnop.resize(110, 25)
    self.CategorieToevoegenKnop.move(nx//2-55, 10)
    self.CategorieToevoegenKnop.clicked.connect(self.voegCategorieToe)

    self.OKknop = QPushButton('OK', self)
    self.OKknop.resize(110, 25)
    self.OKknop.move(nx//2-55, ny-40)
    self.OKknop.clicked.connect(self.accept)

  def setTransactieData(self, transactieData):
    self.transactieData = transactieData
    self.transactieData.sorteerTransacties()
    self.updateCategorieComboBoxen()
    self.updateTransactieLijsten()

  def updateTransactieLijsten(self):
    headers = ['datum', 'bedrag', 'tegenrekening', 'omschrijving']

    categorie1 = self.transactieLijst1Categorie.currentText()
    self.transactieLijst1.clear()
    self.transactieLijst1.addItems(self.transactieData.transactieLijst(categorie1, headers)[2:])

    categorie2 = self.transactieLijst2Categorie.currentText()
    self.transactieLijst2.clear()
    self.transactieLijst2.addItems(self.transactieData.transactieLijst(categorie2, headers)[2:])

  def updateCategorieComboBoxen(self):
    self.transactieLijst1Categorie.clear()
    self.transactieLijst1Categorie.addItems(self.transactieData.categorieOverzicht())
    self.transactieLijst2Categorie.clear()
    self.transactieLijst2Categorie.addItems(self.transactieData.categorieOverzicht())

  def verplaatsLR(self):
    indexen = sorted([x.row() for x in self.transactieLijst1.selectedIndexes()], reverse=True)
    categorieL = self.transactieLijst1Categorie.currentText()
    categorieR = self.transactieLijst2Categorie.currentText()
    for i in indexen:
      self.transactieData.data[categorieR]['transacties'].append(self.transactieData.data[categorieL]['transacties'].pop(i))

    self.transactieData.sorteerTransacties()
    self.updateTransactieLijsten()

  def verplaatsRL(self):
    indexen = sorted([x.row() for x in self.transactieLijst2.selectedIndexes()], reverse=True)
    categorieL = self.transactieLijst1Categorie.currentText()
    categorieR = self.transactieLijst2Categorie.currentText()
    for i in indexen:
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
