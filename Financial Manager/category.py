class category(object) :
    def __init__(self,ratio_default=None) :
        self.ratio_default=ratio_default
        self.ratio=ratio_default
    def getRatio_default(self):
        return self.ratio_default
    def setRatio(self,ratio) :
        self.ratio=ratio
    def setIncome(self,income) :
        self.income=income
    def getRatio(self):
        return self.ratio
    def getIncome(self) :
        return self.income
    def getNominal(self,income) :
        return self.ratio/100*income
    