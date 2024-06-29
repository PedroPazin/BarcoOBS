# Imports go at the top
from microbit import *
from time import sleep
display.off()

# MOTOR
# Os 2 motores da frente
motorPin0 = pin0
motorPin1 = pin1
motorPin2 = pin2
motorPin3 = pin3

# Os 2 motores de tras
motorPin16 = pin16
motorPin15 = pin15
motorPin14 = pin14
motorPin13 = pin13

# BOTÕES
buttonNorth = pin8
buttonSouth = pin9

# Func North
def going_north(_graus, _isNorth):
    if _isNorth: # Esta indo corretamente, todos os motores estao ativos
        # Motores 0 ao 3
        motorPin0.write_digital(1)
        motorPin1.write_digital(0)
        motorPin2.write_digital(1)
        motorPin3.write_digital(0)

        # Motores 10 ao 13
        motorPin16.write_digital(1)
        motorPin15.write_digital(0)
        motorPin14.write_digital(1)
        motorPin13.write_digital(0)
    else: # Nao esta indo corretamente, diminui muito os motores nao nao necessarios para voltar a direçao correta
        motorPin16.write_digital(1)
        motorPin15.write_digital(0)
        motorPin14.write_digital(1)
        motorPin13.write_digital(0)
        if _graus <= 180: # Diminuindo o motor traseiro esquerdo
            percentageToTake = abs(_graus - 10) * (1 / 100)
            motorPin0.write_digital(0)
            motorPin1.write_digital(0)

            # Acionando os motores que serao necessarios para virar (traseiro esquerdo)
            motorPin3.write_digital(1)
            motorPin2.write_digital(0)
        elif _graus > 180: # Diminuindo o motor traseiro direito
            percentageToTake = abs(_graus - 350) * (1 / 100)
            motorPin3.write_digital(0)
            motorPin2.write_digital(0)

            # Acionando os motores que serao necessarios para virar (traseiro direito)
            motorPin0.write_digital(1)
            motorPin1.write_digital(0)


# Going South
def going_south(_graus, _isSouth):
    if _isSouth: # Esta indo corretamente, todos os motores estao ativos
        # Motores 0 ao 3
        motorPin0.write_digital(0)
        motorPin1.write_digital(1)
        motorPin2.write_digital(0)
        motorPin3.write_digital(1)

        # Motores 10 ao 13
        motorPin16.write_digital(0)
        motorPin15.write_digital(1)
        motorPin14.write_digital(0)
        motorPin13.write_digital(1)
    else: # Nao esta indo corretamente, diminui muito os motores nao nao necessarios para voltar a direçao correta
        motorPin0.write_digital(0)
        motorPin1.write_digital(1)
        motorPin2.write_digital(0)
        motorPin3.write_digital(1)

        if _graus <= 180: # Diminuindo o motor dianteiro esquerdo
            percentageToTake = (180 - _graus) * (1 / 100)
            motorPin15.write_digital(0)
            motorPin16.write_digital(0)

            # Acionando os motores necessarios para virar (dianteiro direito)
            motorPin13.write_digital(1)
            motorPin14.write_digital(0)
        elif _graus > 180: # Diminuindo o motor dianteiro direito
            percentageToTake = (_graus - 180) * (1 / 100)
            motorPin13.write_digital(0)
            motorPin14.write_digital(0)

            # Acionandos os motores necessários para virar (dianteiro esquerdo)
            motorPin15.write_digital(1)
            motorPin16.write_digital(0)



graus = 0 # Variavel que recebe os graus da angulaçao
directionToGo = 'N' # Variavel que recebe qual direçao o barco tem que ir
isInDirection = True # Variavel que recebe True caso o barco esteja na angulaçao correta
cont = 0

# Variaveis da bussola
norte = 118

while True:
    graus = compass.heading() # Pegando os graus a todo momento
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
        motorPin0.write_analog(0)
        motorPin1.write_analog(0)
        motorPin2.write_analog(0)
        motorPin3.write_analog(0)

        # Motores 10 ao 13
        motorPin16.write_analog(0)
        motorPin15.write_analog(0)
        motorPin14.write_analog(0)
        motorPin13.write_analog(0)

    if directionToGo == 'N': # Caso ele tenha que ir para o Norte
        isInDirection = True if grausCorreto <= 15 or grausCorreto >= 345 else False

        going_north(grausCorreto, isInDirection) # Func para ir para o norte
    elif directionToGo == 'S': # Caso ele tenha que ir para o Sul
        isInDirection = True if grausCorreto >= 345 or grausCorreto <= 15 else False

        going_south(grausCorreto, isInDirection) # Func para ir para o Sul
