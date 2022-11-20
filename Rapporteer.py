import matplotlib.pyplot as plt
from datetime import datetime

class rapporteerTransactieData():
  def __init__(self):
    self.transactieData = None

  def setTransactieData(self, transactieData):
    self.transactieData = transactieData

  def maakJaarBarPlots(self, jaar, categorie):
    maanden = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']

    tot = []
    inTot = []
    uitTot = []
    aantal = []
    for j in range(12):
      startDatum = datetime(jaar + j//12, j%12+1, 1)
      eindDatum = datetime(jaar + (j+1)//12, (j+1)%12+1, 1)
      subTot, subIn, subUit, subTal = self.transactieData.berekenTotalen(categorie, startDatum, eindDatum)

      tot.append(subTot)
      inTot.append(subIn)
      uitTot.append(-subUit)
      aantal.append(subTal)

    fig, ax = plt.subplots(1)
    ax.bar(maanden, uitTot)
    ax.set_title(f'uitgaven in "{categorie}" in {jaar}')
    plt.show()
    plt.close(fig)

    fig, ax = plt.subplots(1)
    ax.bar(maanden, inTot)
    ax.set_title(f'inkomsten in "{categorie}" in {jaar}')
    plt.show()
    plt.close(fig)


