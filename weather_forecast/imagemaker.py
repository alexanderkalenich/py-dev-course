# -*- coding: utf-8 -*-
import os
import cv2


class ImageMaker:
    """
    Создание и сохранение в файл открыток с погодой.
    """

    def __init__(self, date):
        self.date = date
        self.image_path = f'cards/{date}.jpg'

    def inscription(self, img1, weather):
        color = (0, 0, 0)
        cv2.putText(img1, f'Дата: {self.date}', (150, 50), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
        cv2.putText(img1, f'{weather}', (30, 150), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 1)
        self.save_image(self.date, img1)

    def check_dir(self):
        check_dir = os.path.exists('cards')
        if check_dir:
            return
        else:
            os.mkdir('cards')
            return

    def save_image(self, date, img1):
        self.check_dir()
        cv2.imwrite(self.image_path, img1)

    def show(self, date, img1):
        cv2.imshow(date, img1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def picture(self, weather, logo):
        b, g, r = 0, 0, 0

        if logo == 'облачно':
            logo = 'cloud.jpg'
            b, g, r = 82, 82, 82
        elif logo == 'дождь':
            logo = 'rain.jpg'
            b, g, r = 183, 30, 22
        elif logo == 'солнечно':
            logo = 'sun.jpg'
            b, g, r = 57, 250, 255
        elif logo == 'снег':
            logo = 'snow.jpg'
            b, g, r = 237, 198, 49
        elif logo == 'ясно':
            logo = 'sun.jpg'
            b, g, r = 57, 250, 255

        img1 = cv2.imread('files/probe.jpg')
        img2 = cv2.imread(f'files/weather_img/{logo}')

        vert_line = 0
        color_step = 0

        for _ in range(350):
            img1 = cv2.rectangle(img1, (1 + vert_line, 0), (0 + vert_line, 300),
                                 (b + color_step, g + color_step, r + color_step), -1)

            vert_line += 2
            color_step += 1

        rows, cols, channels = img2.shape
        roi = img1[0:rows, 0:cols]

        img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)

        mask_inv = cv2.bitwise_not(mask)

        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

        dst = cv2.add(img1_bg, img2_fg)
        img1[0:rows, 0:cols] = dst

        self.inscription(img1, weather)
        return self.image_path
