from varasto import Varasto


def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    tulosta_luonti(mehua, olutta)
    tulosta_getterit(olutta)
    tulosta_setterit(mehua)
    tulosta_virhetilanteet(mehua, olutta)


def tulosta_luonti(mehua, olutta):
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")


def tulosta_getterit(olutta):
    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")


def tulosta_setterit(mehua):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")


def tulosta_virhetilanteet(mehua, olutta):
    print("Virhetilanteita:")
    tulosta_negatiiviset_arvot()
    tulosta_ylitaytto(olutta)
    tulosta_negatiiviset_operaatiot(mehua, olutta)


def tulosta_negatiiviset_operaatiot(mehua, olutta):
    tulosta_negatiivinen_lisays(mehua)
    tulosta_liika_otto(olutta, mehua)


def tulosta_negatiiviset_arvot():
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)
    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)


def tulosta_ylitaytto(olutta):
    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")


def tulosta_negatiivinen_lisays(mehua):
    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def tulosta_liika_otto(olutta, mehua):
    testaa_olut_ylotto(olutta)
    testaa_mehu_negatiivinen_otto(mehua)


def testaa_olut_ylotto(olutta):
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")


def testaa_mehu_negatiivinen_otto(mehua):
    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


if __name__ == "__main__":
    main()
