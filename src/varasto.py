class Varasto:
    def __init__(self, tilavuus, alku_saldo=0):
        self.tilavuus = self._validoi_tilavuus(tilavuus)
        self.saldo = self._validoi_saldo(alku_saldo, self.tilavuus)

    def _validoi_tilavuus(self, tilavuus):
        if tilavuus > 0.0:
            return tilavuus
        return 0.0

    def _validoi_saldo(self, alku_saldo, tilavuus):
        if alku_saldo < 0.0:
            return 0.0
        if alku_saldo <= tilavuus:
            return alku_saldo
        return tilavuus

    def paljonko_mahtuu(self):
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            return self._ota_kaikki()
        self.saldo = self.saldo - maara
        return maara

    def _ota_kaikki(self):
        kaikki = self.saldo
        self.saldo = 0.0
        return kaikki

    def __str__(self):
        vapaa_tila = self.paljonko_mahtuu()
        return f"saldo = {self.saldo}, vielä tilaa {vapaa_tila}"
