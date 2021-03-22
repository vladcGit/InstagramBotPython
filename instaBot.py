from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.firefox.options import Options
from os import remove, rename
from cryptography.fernet import Fernet
import sys

options = Options()
options.headless = True


# modul criptare username si parola

def write_key():
    key = Fernet.generate_key()
    with open('key', 'wb')as key_file:
        key_file.write(key)


def load_key():
    try:
        return open("key", "rb").read()
    except:
        write_key()
        return open("key", "rb").read()


def autentificare():
    key = load_key()
    f = Fernet(key)
    try:
        fisier = open('autentificare.encrypted', 'rb')
        try:
            decrypted = f.decrypt(fisier.read())
            fisier.close()
            return decrypted
        except:
            print("Cheie gresita")
            exit(1)
    except:
        user = input("Introdu numele de utilizator:\n")
        parola = input("Introdu parola:\n")
        message = (user + ' ' + parola).encode()
        encrypted = f.encrypt(message)
        fisier = open('autentificare.encrypted', 'wb')
        fisier.write(encrypted)
        fisier.close()
        return message


# sterge datele din geckokdriver.log la fiecare pornire a aplicatiei
def sterge_log_browser():
    try:
        f = open('geckodriver.log', 'w')
        f.close()
    except:
        pass


# RNG bazat pe ora actuala
def random_number(cazuri_posibile):
    ms = str(datetime.now()).split(':')[2].split('.')[1]
    return int(ms) % cazuri_posibile


# functia principala de sleep
def somn(x):
    print("Sleeping " + str(x) + " mins, until " +
          str(datetime.now() + timedelta(hours=0, minutes=x)) + '\n')
    sleep(x * 60)


# functia care ia un numar de forma 4,768 sau 12.2k
# si il converteste in format int

def convertireNumar(nr):
    if nr[-1] == 'k':
        nr = nr.split('k')
        return int((float(nr[0]) * 1000))
    if nr.find(',') != -1:
        nr = nr.split(',')
        return int(nr[0]) * 1000 + int(nr[1])
    return int(nr)


# functia de iesit in cas de eroare
def force_exit(exceptie, bot):
    bot.quit()
    sys.exit(str(exceptie))


# clasa principala

class instaBot:
    # constructor
    def __init__(self, username, parola):
        self.username = username
        self.parola = parola

        # Varianta in care vrem sa vedem ce se intampla in browser
        self.bot = webdriver.Firefox()
        # Varianta in care nu vrem sa vedem browserul
        # self.bot=webdriver.Firefox(options=options)

    # login in contul de insta
    def login(self):

        # navigare la pagina principala instagram
        self.bot.get('https://www.instagram.com/?hl=ro')
        sleep(3)

        # pop-up enervant
        self.bot.find_element_by_xpath(
            "//button[contains(text(), 'Accept')]").click()

        # completare textbox pentru user si parola
        nume_de_utilizator = self.bot.find_element_by_name('username')
        parola = self.bot.find_element_by_name('password')
        nume_de_utilizator.send_keys(self.username)
        parola.send_keys(self.parola)
        parola.send_keys(Keys.RETURN)

        sleep(5)

        # pop-up uri enervante
        try:
            self.bot.find_element_by_xpath(
                "//button[contains(text(), 'Nu acum')]").click()
        except:
            pass
        sleep(5)
        try:
            self.bot.find_element_by_xpath(
                "//button[contains(text(), 'Not Now')]").click()
        except:
            pass

    # functia care verifica lista de followeri a unui user
    # care se opreste cand itereaza prin lista de followeri
    # de -limita_iterari- ori
    def veziFolloweri(self, nume_user, limita_iterari=100):
        names = []
        sleep(5)
        self.bot.get('https://www.instagram.com/' + nume_user)
        sleep(3)

        # apasa pe butonul cu textul 'followers'
        try:
            self.bot.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        except Exception as ex:
            print("Eroare la obtinerea followerilor pentru user ul " + nume_user)
            force_exit(ex, self.bot)

        sleep(2)
        # iterare prin lista useri
        try:
            scroll_box = self.bot.find_element_by_class_name('isgrP')
            last_ht, ht, x = 0, 1, 0
            while last_ht != ht and x < limita_iterari:
                last_ht = ht
                sleep(2)
                ht = self.bot.execute_script("""
                arguments[0].scrollTo(0,arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
                x += 1
            links = scroll_box.find_elements_by_tag_name('a')
            names = [name.text for name in links if name.text != '']
            sleep(2)
        except Exception as ex:
            print(ex)
        return names

    # functia care verifica lista de followeri a unui user
    def veziFollowing(self, nume_user):
        names = []
        self.bot.get('https://www.instagram.com/' + nume_user)
        sleep(5)

        # apasa pe butonul cu textul 'following'
        try:
            self.bot.find_element_by_xpath(
                "//a[contains(@href, '/following')]").click()
        except Exception as ex:
            print(ex)

        sleep(2)

        # iterare prin lista useri
        try:
            scroll_box = self.bot.find_element_by_class_name('isgrP')
            last_ht, ht = 0, 1
            while last_ht != ht:
                last_ht = ht
                sleep(2)
                ht = self.bot.execute_script("""
                arguments[0].scrollTo(0,arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
            links = scroll_box.find_elements_by_tag_name('a')
            names = [name.text for name in links if name.text != '']

        except Exception as ex:
            print(ex)

        sleep(2)
        return names

    # follow un user si scriere in fisier, pleaca
    # de la asumptia ca pagina user-ului era deja
    # deschisa si in focus
    def followUser(self, nume_user, f):
        sleep(random_number(3) + 2)

        self.bot.find_element_by_xpath(
            "//button[contains(text(), 'Follow')]").click()
        mesaj = nume_user + ' ' + str(datetime.now()) + '\n'
        print('Followed ' + mesaj, end='')
        f.write(mesaj)

        sleep(random_number(10))

    # unfollow un user
    def unfollowUser(self, nume_user):
        self.bot.get('https://www.instagram.com/' + nume_user)
        sleep(random_number(5) + 2)
        # cazul in care a dat accept la follow
        try:
            self.bot.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button").click()
            sleep(2)
            self.bot.find_element_by_xpath(
                "//button[contains(text(), 'Unfollow')]").click()
        # cazul in care nu a dat accept la follow
        except:
            try:
                self.bot.find_element_by_xpath(
                    "//button[contains(text(), 'Requested')]").click()
                self.bot.find_element_by_xpath(
                    "//button[contains(text(), 'Unfollow')]").click()
            except:
                self.bot.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button').click()
                self.bot.find_element_by_xpath(
                    "//button[contains(text(), 'Unfollow')]").click()

        sleep(random_number(10))

    # obtine nr de followeri si following al unui user
    def getInformatiiUser(self):

        # lista ar trebui sa contina nr de postari,
        # de followeri si de following
        lista = self.bot.find_elements_by_class_name('g47SY')
        if len(lista) != 3:
            return -1, -1
        # returnare valori
        return convertireNumar(lista[1].text), convertireNumar(lista[2].text)

    # functia principala de obtinut followeri
    def furaFolloweri(self, names):
        # deschidere fisier unde se da follow
        f = open('lista_follow.txt', 'a')
        # se seteaza o limita maxima de followeri pe incercare
        limita = 30 - random_number(9)
        x = 0
        # follow propriu-zis
        for name in names:
            if name != '' and x < limita:
                try:
                    self.bot.get('https://www.instagram.com/' + name)
                    sleep(3)
                    # obtinere informatii user din lista
                    nr_followeri, nr_following = self.getInformatiiUser()
                    # verificare daca e bun pentru follow-unfollow
                    if nr_followeri > 0 and nr_following > 100 and nr_followeri / nr_following < 0.5:
                        self.followUser(name, f)
                        x += 1
                except Exception as ex:
                    print(ex)
            else:
                break
        f.close()
        print("\nTerminat de furat followeri\n")

    # functia principala de dat unfollow
    def unfollowInMasa(self):
        # eliminare din fisier utilizatorii care au primit unfollow
        f = open('lista_follow.txt', 'r')
        g = open('temp', 'w')
        sleep(2)
        # lista cu datele despre unfollower
        unfollower_nume, unfollower_ora = [], []
        for linie in f.readlines():
            sir = linie.split(' ')[0]
            if sir != '':
                # obtinere date despre ora la care s-a dat follow
                ora = linie[len(sir) + 1:].strip()
                ora = datetime.strptime(ora, '%Y-%m-%d %H:%M:%S.%f')
                unfollower_nume.append(sir)
                unfollower_ora.append(ora)

        # unfollow propriu-zis

        # setare limita numar de oameni unfollow
        limita = 20 - random_number(4)
        nr_oameni_unfollowed = 0
        for i in range(len(unfollower_nume)):

            nume_user = unfollower_nume[i]
            ora_user = unfollower_ora[i]

            # verifica daca follow-ul a fost dat in mai mult de o zi
            # si daca limita nu a fost depasita
            if (datetime.now() - ora_user).days > 0 and nr_oameni_unfollowed < limita:
                try:
                    self.unfollowUser(nume_user)
                    nr_oameni_unfollowed += 1
                    print('Unfollowed ' + nume_user.strip())
                    sleep(random_number(6) + 2)
                except Exception as ex:
                    print('User-ul ' + nume_user +
                          ' nu (mai) exista sau nu a dat accept la follow')

            # daca user-ul nu a primit unfollow il rescriem in fisier
            else:
                g.write(nume_user + ' ' + str(ora_user) + '\n')

        # inlocuire fisiere
        f.close()
        g.close()
        remove('lista_follow.txt')
        rename('temp', 'lista_follow.txt')
        print("\nTerminat de dat unfollow\n")

    # functia care da logout din cont
    def logout(self):
        # butonul cu poza de profil
        self.bot.find_element_by_xpath(
            '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        sleep(2)
        # butonul de logout
        self.bot.find_element_by_xpath(
            "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div").click()
        sleep(3)
