# Imports go at the top
from microbit import *
from time import sleep
display.off()

class Motor: # Classe que recebera os motores e suas funções
    def __init__(self, pinM1, pinM2):
        self.pinM1 = pinM1
        self.pinM2 = pinM2

    def forward(self):
        self.pinM1.write_digital(1)
        self.pinM2.write_digital(0)

    def backwards(self):
        self.pinM1.write_digital(0)
        self.pinM2.write_digital(1)

    def stop(self):
        self.pinM1.write_digital(0)
        self.pinM2.write_digital(0)

# Motores
frontMotor1 = Motor(pin0, pin1)
frontMotor2 = Motor(pin2, pin3)
backMotor1 = Motor(pin16, pin15)
backMotor2 = Motor(pin14, pin13)

# Func North
def going_north(_graus, _isNorth):
    if _isNorth: # Esta indo corretamente, todos os motores estao ativos
        # Motores dianteiros
        frontMotor1.forward()
        frontMotor2.forward()

        # Motores traseiros
        backMotor1.forward()
        backMotor2.forward()
    else: # Nao esta indo corretamente
        backMotor1.forward()
        backMotor2.forward()
        if _graus <= 180: # Desligando o motor traseiro esquerdo
            frontMotor1.stop()
            backMotor2.stop()

            # Acionando os motores que serao necessarios para virar (traseiro esquer
            frontMotor2.forward()
        elif _graus > 180: # Desligando o motor traseiro direito
            frontMotor2.stop()
            backMotor1.stop()

            # Acionando os motores que serao necessarios para virar (traseiro direito)
            frontMotor1.forward()

# Going South
def going_south(_graus, _isSouth):
    if _isSouth: # Esta indo corretamente, todos os motores estao ativos
        # Motores 0 ao 3
        frontMotor1.backwards()
        frontMotor2.backwards()

        # Motores 10 ao 13
        backMotor1.backwards()
        backMotor2.backwards()
    else: # Nao esta indo corretamente
        frontMotor1.backwards()
        frontMotor2.backwards()

        if _graus <= 180: # Desligando o motor traseiro esquerdo
            backMotor1.stop()
            frontMotor2.forward()

            # Acionando os motores necessarios para virar (traseiro direito)
            backMotor2.backwards()
        elif _graus > 180: # Desligando o motor traseiro direito
            backMotor2.stop()
            frontMotor1.forward()

            # Acionandos os motores necessários para virar (dianteiro esquerdo)
            backMotor1.backwards()



graus = 0 # Variavel que recebe os graus da angulaçao
directionToGo = 'N' # Variavel que recebe qual direçao o barco tem que ir
isInDirection = True # Variavel que recebe True caso o barco esteja na angulaçao correta
cont = 0

# Variaveis da bussola
norte = 130

# BOTÕES
buttonNorth = pin8
buttonSouth = pin9

while True:
    graus = compass.heading() # Pegando os graus a todo momento
    # Setando qual é o norte, nao importando o que aparece na bussola
    grausCorreto = graus - norte if graus >= norte else 360 + (graus - norte)

    if button_a.is_pressed():
        print('graus: ' + str(graus))
        directionToGo = 'N'
    else:
        print(grausCorreto)

    if button_b.is_pressed():
        print(directionToGo)

    sleep(0.01)
    # Botões

    if buttonNorth.read_digital() == 1 and directionToGo == 'N': # Caso o botao da frente seja clicado, ira desligar este botao e ligar o de tras
        print('sul')
        directionToGo = 'S' # Colocara como Sul a direçao que o barco tera que seguir
    if buttonSouth.read_digital() == 1 and directionToGo == 'S': # Caso o botao de tras seja clicado, tudo ira parar
        print('parou')
        directionToGo = 'N/A'
        # Motores 0 ao 3
        frontMotor1.stop()
        frontMotor2.stop()

        # Motores 10 ao 13
        backMotor1.stop()
        backMotor2.stop()

    if directionToGo == 'N': # Caso ele tenha que ir para o Norte
        isInDirection = True if grausCorreto <= 7 or grausCorreto >= 358 else False

        going_north(grausCorreto, isInDirection) # Func para ir para o norte
    elif directionToGo == 'S': # Caso ele tenha que ir para o Sul
        isInDirection = True if grausCorreto >= 356 or grausCorreto <= 7 else False

        going_south(grausCorreto, isInDirection) # Func para ir para o Sul
