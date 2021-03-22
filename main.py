from instaBot import *
from os import system

# decriptare user si parola
sir_date_autentificare = autentificare().decode('ascii')
user, parola = sir_date_autentificare.split(
)[0], sir_date_autentificare.split()[1]


# functia principala de follow
def one():
    for i in range(5):
        driver = instaBot(user, parola)
        driver.login()
        influencer = lista_influenceri[random_number(len(lista_influenceri))]
        names = driver.veziFolloweri(influencer, 20)
        driver.furaFolloweri(names)
        driver.logout()
        driver.bot.quit()
        if i < 4:
            somn(60)


# functia principala de unfollow
def two():
    for i in range(5):
        driver = instaBot(user, parola)
        driver.login()
        driver.unfollowInMasa()
        driver.logout()
        driver.bot.quit()
        if i < 4:
            somn(60)


# functia care salveaza toti userii pe care ii am la following
def three():
    driver = instaBot(user, parola)
    driver.login()
    # toti userii pe care ii am la following
    names = driver.veziFollowing(driver.username)
    # toti userii pe care ii am la following minus cateva vedete
    unfolloweri = [pers for pers in names if user not in lista_vedete_following]
    # scriere in fisier
    f = open('lista_follow.txt', 'w')
    for unfollower in unfolloweri:
        # se scrie fiecare user cu data de ieri ca data la care am dat follow
        ziua_de_ieri = datetime.now() - timedelta(1)
        f.write(unfollower + ' ' + str(ziua_de_ieri) + '\n')
    f.close()
    driver.bot.refresh()
    sleep(3)
    driver.logout()
    driver.bot.quit()


# functia parser care alege corect optiunea
def parser(argument):
    system('cls')
    # se asigura ca optiunea e valida
    if argument not in (1, 2, 3):
        raise Exception('Nu exista optiunea aleasa')
    # switch propriu zis
    switcher = {
        1: one,
        2: two,
        3: three
    }
    func = switcher.get(argument)
    func()


# declarari de inceput
lista_influenceri = ['katrinakaif', 'nehakakkar', 'jacquelinef143', 'aliaabhatt',
                     'deepikapadukone', 'virat.kohli', 'priyankachopra', 'shraddhakapoor']

lista_vedete_following = ['nyxcosmetics_romania', 'raesremmurd', 'wizkhalifa', 'zacefron',
                          'justinbieber', 'realmadrid', 'vanessahudgens', 'leonardodicaprio', 'katyperry',
                          'kendalljenner', 'chloegmoretz', 'equipedefrance', 'mosalah', 'mango', 'mileycyrus',
                          'gal_gadot', 'therock', 'katrinakaif', 'sashapieterse', 'instagram', 'toni.kr8s']

sterge_log_browser()

system('color 9f')
system('cls')

print(
    '''
        Alegeti un numar intre 1 si 3:\n\n
        1.Da follow unor noi persoane
        2.Da unfollow unor persoane
        3.Primeste lista cu toti cei carora trebuie sa le dai unfollow
        
        Alege: 
        '''
)
try:
    parser(int(input()))
except Exception as ex:
    print(ex)

print("\nAplicatia se inchide")
