# TEE PELI TÄHÄN
# Peli

import pygame
import random
import math

class Luolasto:
    def __init__(self):
        pygame.init()

        self.naytto_korkeus = 480
        self.naytto_leveys = 640
        self.naytto = pygame.display.set_mode((self.naytto_leveys, self.naytto_korkeus))
        self.fontti = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("Luolasto")
        self.lataa_kuvat()
        self.robo_koko = [self.kuvat[3].get_width(), self.kuvat[3].get_height()]
        self.uusi_peli()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["hirvio", "kolikko", "ovi", "robo"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))

    def uusi_peli(self):
        self.robo_paikka = [100, 300]
        self.hirvio_paikka = [100, 100]
        # 1 vakikolikko 2 arvottua
        self.kolikot = [[130, 90], [random.randint(150, self.naytto_leveys-50), random.randint(150, self.naytto_korkeus-50)], [random.randint(150, self.naytto_leveys-50), random.randint(150, self.naytto_korkeus-50)]]
        self.ovi_paikka = [320, 0]
        self.portsari_paikka = [320, 20]

        self.etaisyys_roboon = [None, None]
        self.oikealle = False
        self.vasemmalle = False
        self.alas = False
        self.ylos = False
        self.kyhny = 0
        self.energia = 63
        self.hirvio_nopeus = 0.5
        self.kello = pygame.time.Clock()
        self.silmukka()


    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            if not self.peli_ohi():
                self.liikkuva_hirvio()
                self.piirra_naytto()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
                
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
                

            if tapahtuma.type == pygame.QUIT:
                exit()
        
        if self.vasemmalle:
            if self.robo_paikka[0] > 0:
                self.liiku(-1, 0)
        if self.oikealle:
            if self.robo_paikka[0] < self.naytto_leveys - self.kuvat[3].get_width():
                self.liiku(1, 0)
        if self.ylos:
            if self.robo_paikka[1] > 64:
                self.liiku(0, -1)
        if self.alas:
            if self.robo_paikka[1] < self.naytto_korkeus - self.kuvat[3].get_height():
                self.liiku(0, 1)

        for kolikko in self.kolikot:
            if math.sqrt((kolikko[0]+self.kuvat[1].get_width()/2-(self.robo_paikka[0]+self.kuvat[3].get_width()/2))**2 + (kolikko[1]+self.kuvat[1].get_height()/2-(self.robo_paikka[1]+self.kuvat[3].get_height()/2))**2) < 60:
                kolikko[0] = -100
                kolikko[1] = -100
                self.kyhny = self.kyhny + 1

        self.laske_energia()
        self.peli_ohi()
    
    def laske_energia(self):
        if self.peli_ohi():
            return
        if math.sqrt((self.hirvio_paikka[0] + self.kuvat[0].get_width()/2-(self.robo_paikka[0]+self.kuvat[3].get_width()/2))**2 + (self.hirvio_paikka[1]+self.kuvat[0].get_height()/2-(self.robo_paikka[1]+self.kuvat[3].get_height()/2))**2) < 40:
            self.energia = self.energia - 1
        
    
    def liiku(self, liike_x, liike_y):
        if self.peli_ohi():
            return
        self.robo_paikka = self.robo_paikka[0] + liike_x, self.robo_paikka[1] + liike_y
        # print(f"Robon paikka {self.robo_paikka}")


    def liikkuva_hirvio(self):
        # hirvio liikkuu hirvio_nopeus yksikköä x tai y suunnassa robottia kohden
        self.etaisyys_roboon[0] = self.hirvio_paikka[0] - self.robo_paikka[0]
        self.etaisyys_roboon[1] = self.hirvio_paikka[1] - self.robo_paikka[1]
        if abs(self.etaisyys_roboon[0]) > abs(self.etaisyys_roboon[1]):
            if self.etaisyys_roboon[0] < 0:
                self.hirvio_paikka[0] = self.hirvio_paikka[0] + self.hirvio_nopeus
            else:
                self.hirvio_paikka[0] = self.hirvio_paikka[0] - self.hirvio_nopeus
        else:
            if self.etaisyys_roboon[1] < 0:
                self.hirvio_paikka[1] = self.hirvio_paikka[1] + self.hirvio_nopeus
            else:
                self.hirvio_paikka[1] = self.hirvio_paikka[1] - self.hirvio_nopeus

    def piirra_naytto(self):     
        self.naytto.fill((0, 128, 0))
        self.naytto.blit(self.kuvat[3], (self.robo_paikka))
        self.naytto.blit(self.kuvat[0], (self.hirvio_paikka))
        self.naytto.blit(self.kuvat[1], (self.kolikot[0]))
        self.naytto.blit(self.kuvat[1], (self.kolikot[1]))
        self.naytto.blit(self.kuvat[1], (self.kolikot[2]))
        self.naytto.blit(self.kuvat[2], (self.ovi_paikka))
        self.naytto.blit(self.kuvat[0], (self.portsari_paikka))
        
        teksti = self.fontti.render("Kyhnyä: " + str(self.kyhny), True, (0, 0, 0))
        self.naytto.blit(teksti, (25, 10))
        teksti = self.fontti.render("Emälät: " + str(self.energia), True, (0, 0, 0))
        self.naytto.blit(teksti, (25, 40))
        teksti = self.fontti.render("F2 = uusi peli", True, (128, 0, 0))
        self.naytto.blit(teksti, (140, 10))
        teksti = self.fontti.render("Esc = sulje peli", True, (128, 0, 0))
        self.naytto.blit(teksti, (140, 40))
        teksti = self.fontti.render("Ohje: Välttele huligaania,", True, (255, 0, 128))
        self.naytto.blit(teksti, (380, 10))
        teksti = self.fontti.render("kerää kolikot ja lahjo portsari.", True, (255, 0, 128))
        self.naytto.blit(teksti, (380, 40))


        self.kello.tick(60)
        pygame.display.flip()

    def peli_ohi(self):
        if self.energia < 1:
            self.naytto.fill((0, 128, 0))
            teksti = self.fontti.render("Kyhnyä: " + str(self.kyhny), True, (0, 0, 0))
            self.naytto.blit(teksti, (25, 10))
            teksti = self.fontti.render("Emälät: " + str(self.energia), True, (255, 0, 0))
            self.naytto.blit(teksti, (25, 40))
            teksti = self.fontti.render("F2 = uusi peli", True, (128, 0, 0))
            self.naytto.blit(teksti, (140, 10))
            teksti = self.fontti.render("Esc = sulje peli", True, (128, 0, 0))
            self.naytto.blit(teksti, (140, 40))
            teksti = self.fontti.render("Ohje: Välttele huligaania,", True, (255, 0, 128))
            self.naytto.blit(teksti, (380, 10))
            teksti = self.fontti.render("kerää kolikot ja lahjo portsari.", True, (255, 0, 128))
            self.naytto.blit(teksti, (380, 40))
            teksti = self.fontti.render("Emälät loppui :(", True, (255, 0, 0))
            self.naytto.blit(teksti, (200, 255))
            pygame.display.flip()
            return True

        if self.kyhny >= 3:
            if self.robo_paikka[1] <=64:
                if 295 < self.robo_paikka[0] < 330:
                    self.naytto.fill((0, 128, 0))
                    teksti = self.fontti.render("F2 = uusi peli", True, (0, 0, 0))
                    self.naytto.blit(teksti, (200, 55))
                    teksti = self.fontti.render("Esc = sulje peli", True, (0, 0, 0))
                    self.naytto.blit(teksti, (400, 55))
                    teksti = self.fontti.render("Hyvin tehty!", True, (0, 0, 0))
                    self.naytto.blit(teksti, (200, 120))
                    teksti = self.fontti.render("Sisäänpääsy ULOS OK :)", True, (0, 0, 0))
                    self.naytto.blit(teksti, (200, 255))
                    pygame.display.flip()
                    return True
        return False

if __name__ == "__main__":
    Luolasto()
