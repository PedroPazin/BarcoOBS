# Imports go at the top
from microbit import *
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
buttonNorthPin6 = pin6
buttonSouthPin7 = pin7

# Func North
def going_north(_graus, _isNorth):
    if(_isNorth): # Esta indo corretamente, todos os motores estao ativos
        # Motores 0 ao 3
        motorPin0.write_analog(1023)
        motorPin1.write_analog(100)
        motorPin2.write_analog(100)
        motorPin3.write_analog(1023)

        # Motores 10 ao 13
        motorPin16.write_analog(1023)
        motorPin15.write_analog(100)
        motorPin14.write_analog(1023)
        motorPin13.write_analog(100)
    else: # Nao esta indo corretamente, diminui muito os motores nao nao necessarios para voltar a direçao correta
        motorPin16.write_analog(400)
        motorPin15.write_analog(100)
        motorPin14.write_analog(400)
        motorPin13.write_analog(100)
        percentageToTake = _graus * (3 / 100) if _graus <= 180 else (360 - _graus) * (3 / 100) # A cada grau na direçao errada, ira ser diminuido 2% do motor
        if(_graus <= 180): # Diminuindo o motor traseiro esquerdo
            motorPin3.write_analog(1023 - (1023 * percentageToTake/10))
            motorPin2.write_analog(100)

            # Acionando os motores que serao necessarios para virar (traseiro direito)
            motorPin0.write_analog(1023)
            motorPin1.write_analog(100)
        elif(_graus > 180): # Diminuindo o motor traseiro direito
            motorPin0.write_analog(1023 - (1023 * percentageToTake/10))
            motorPin1.write_analog(100)

            # Acionando os motores que serao necessarios para virar (traseiro esquerdo)
            motorPin3.write_analog(1023)
            motorPin2.write_analog(100)

# Going South
def going_south(_graus, _isSouth):
        if(_isSouth): # Esta indo corretamente, todos os motores estao ativos
            # Motores 0 ao 3
            motorPin0.write_analog(100)
            motorPin1.write_analog(1023)
            motorPin2.write_analog(1023)
            motorPin3.write_analog(100)

            # Motores 10 ao 13
            motorPin16.write_analog(100)
            motorPin15.write_analog(1023)
            motorPin14.write_analog(1023)
            motorPin13.write_analog(100)
        else: # Nao esta indo corretamente, diminui muito os motores nao nao necessarios para voltar a direçao correta
            motorPin0.write_analog(100)
            motorPin1.write_analog(400)
            motorPin2.write_analog(400)
            motorPin3.write_analog(100)
            percentageToTake = (180 - _graus) * (3 / 100) if _graus <= 180 else (_graus - 180) * (3 / 100) # A cada grau na direçao errada, ira ser diminuido 2% do motor
            if(_graus >= 0 and _graus < 165): # Diminuindo o motor dianteiro esquerdo
                motorPin14.write_analog(1023 - (1023 * percentageToTake/10))
                motorPin13.write_analog(100)

                # Acionando os motores necessarios para virar (dianteiro direito)
                motorPin15.write_analog(1023)
                motorPin16.write_analog(100)
            elif(_graus <= 359 and _graus > 195): # Diminuindo o motor dianteiro direito
                motorPin15.write_analog(1023 - (1023 * percentageToTake/10))
                motorPin16.write_analog(100)

                # Acionandos os motores necessários para virar (dianteiro esquerdo)
                motorPin14.write_analog(1023)
                motorPin13.write_analog(100)



graus = 0 # Variavel que recebe os graus da angulaçao
directionToGo = 'N' # Variavel que recebe qual direçao o barco tem que ir
isInDirection = True # Variavel que recebe True caso o barco esteja na angulaçao correta
cont = 0
while True:
    if(button_a.was_pressed()): # Ao ser pressionado, ira voltar para as funcionalidades iniciais
        directionToGo = 'N'
        compass.calibrate()
    if button_b.is_pressed():
        print(directionToGo)

    graus = compass.heading() # Pegando os graus a todo momento
    print(graus)
    # Botões

    if(buttonNorthPin6.read_digital() == 1 and directionToGo == 'N' and cont == 1): # Caso o botao da frente seja clicado, ira desligar este botao e ligar o de tras
        print('sul')
        directionToGo = 'S' # Colocara como Sul a direçao que o barco tera que seguir
    elif(buttonSouthPin7.read_digital() == 1 and directionToGo == 'S'): # Caso o botao de tras seja clicado, tudo ira parar
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
    cont = 1
    if(directionToGo == 'N'): # Caso ele tenha que ir para o Norte
        isInDirection = True if(graus <= 15 or graus >= 345) else False

        going_north(graus, isInDirection) # Func para ir para o norte
    elif(directionToGo == 'S'): # Caso ele tenha que ir para o Sul
        isInDirection = True if(graus >= 165 and graus <= 195) else False

        going_south(graus, isInDirection) # Func para ir para o Sul

