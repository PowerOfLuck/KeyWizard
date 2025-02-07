import keyboard
import time


def use_keys(keylist):
    points_list = len(keylist) - 1
    points = 0

    for i in keylist:
        try:
            if points <= points_list:
                if i == "enter":
                    keyboard.press_and_release('enter')
                elif isinstance(i, (float, int)):
                    print('int', i)
                    time.sleep(i)

                elif isinstance(i, str) and len(i) == 1:
                    # keyboard.write(i)
                    keyboard.press_and_release(i)


                elif i.startswith('ctrl:') and len(i) == 6:
                    line_first_point = str(i[5:])
                    line_first_point = line_first_point[0]
                    keyboard.press_and_release('ctrl+' + line_first_point)

                elif i.startswith('shift:') and len(i) == 7:
                    line_first_point = str(i[6:])
                    line_first_point = line_first_point[0]
                    keyboard.press_and_release('shift+' + line_first_point)

                elif i.startswith('alt:') and len(i) == 5:
                    line_first_point = str(i[4:])
                    line_first_point = line_first_point[0]
                    keyboard.press_and_release('alt+' + line_first_point)

                points += 1
            else:
                print('подсчет окончен')

        except Exception as k:
            print(f"Ошибка {k}")


def read_keys():
        keylist = []
        with open('keylist.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('key:') and len(line) > 5:
                    line_first_point = str(line[5:])
                    line_first_point = line_first_point[0]
                    keylist.append(line_first_point)

                elif line.startswith('ctrl:') and len(line) > 6:
                    line_first_point = str(line[6:])
                    line_first_point = line_first_point[0]
                    keylist.append('ctrl:' + line_first_point)

                elif line.startswith('shift:') and len(line) > 7:
                    line_first_point = str(line[7:])
                    line_first_point = line_first_point[0]
                    keylist.append('shift:' + line_first_point)

                elif line.startswith('alt:') and len(line) > 5:
                    line_first_point = str(line[5:])
                    line_first_point = line_first_point[0]
                    keylist.append('alt:' + line_first_point)

                elif line.startswith('time:') and len(line) > 6:
                    keylist.append(float(line[6:]))

                elif line.startswith('enter'):
                    keylist.append(line)



        print('keys', keylist)
        use_keys(keylist)

def keyboard_check(is_running):

    activate = '-'
    with open('keylist.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('activate:') and len(line) > 10:
                activate = line[10:]
                activate = activate[0]

    print(f"Горячая клавиша {activate} активна. Ожидание...")



    while is_running():
        if keyboard.is_pressed(activate):
            read_keys()
        time.sleep(0.1)


