# -*- encoding: utf-8 -*-

# Author:   Hengyu Jiang
# Time:     2021/2/14 14:10
# Email:    hengyujiang.njust.edu.cn
# Project:  MontageTransform
# File:     MontageChanger.py
# Product:  PyCharm
# Desc:     


import os
import cv2 as cv
from copy import deepcopy


class MonTageTransformer(object):
    __DIR_IMAGES = None             # dir in which images to save
    __DIR_IMAGES_SRC = None         # dir in which the processed component images to save
    __DIR_DATASET = None            # dir in which the original components images is saved
    __DIR_LOG = None                # dir in which the logs to save
    __LOG_FOUT = None
    __TARGET_SHAPE = None
    __RESIZE_SHAPE_DATASET = None
    __RESIZE_SHAPE_TARGET = None

    __hist_dict = None
    __image_target = None
    __generate_save_name = None
    __mixmup_weights = None
    __mixup_save_name = None

    __is_generate = True
    __is_mixup = True
    __is_resize_target = False

    def __init__(self, path_image_target, resize_shape_dataset, dir_images, dir_images_src,
                 dir_dataset, dir_log, generate_save_name, is_generate=True, is_mixup=True, is_resize_target=False,
                 mixup_save_name=None, mixup_weights=None, resize_shape_target=None):
        super(MonTageTransformer, self).__init__()

        self.__RESIZE_SHAPE_TARGET = resize_shape_target
        self.__RESIZE_SHAPE_DATASET = resize_shape_dataset
        self.__DIR_IMAGES = dir_images
        self.__DIR_IMAGES_SRC = dir_images_src
        self.__DIR_DATASET = dir_dataset
        self.__DIR_LOG = dir_log

        self.mkdirs()

        self.__image_target = cv.imread(path_image_target)
        self.__TARGET_SHAPE = self.__image_target.shape
        self.__generate_save_name = generate_save_name
        self.__is_generate = is_generate
        self.__is_mixup = is_mixup
        self.__is_resize_target = is_resize_target
        self.__mixup_save_name = mixup_save_name
        self.__mixmup_weights = mixup_weights

        self.__LOG_FOUT = open(os.path.join(self.__DIR_LOG, 'log.txt'), 'w')

    def mkdirs(self):
        """
        check the needed dirs if exist
        :return:
        """
        for dir_ in [self.__DIR_LOG, self.__DIR_IMAGES, self.__DIR_IMAGES_SRC]:
            if not os.path.exists(dir_):
                os.makedirs(dir_)

    def log_string(self, out_str):
        """
        保存日志
        :param out_str:
        """
        self.__LOG_FOUT.write(out_str + '\n')
        self.__LOG_FOUT.flush()
        print(out_str)

    def gen_all_images_src(self):
        """
        将数据集中的所有jpg图像resize到25x25并存入DIR_IMAGES_SRC
        """
        self.log_string('>> gen_all_images_src ...')
        cnt = 0
        for dir_cur in os.listdir(self.__DIR_DATASET):
            self.log_string('>> extracting from {}'.format(os.path.join(self.__DIR_DATASET, dir_cur)))
            for file in os.listdir(os.path.join(self.__DIR_DATASET, dir_cur)):
                img = cv.imread(os.path.join(self.__DIR_DATASET, dir_cur) + '/' + file)
                save_name = self.__DIR_IMAGES_SRC + 'image-{}.jpg'.format(cnt)
                img_resized = cv.resize(img, self.__RESIZE_SHAPE_DATASET)
                self.log_string('>> writing to {}'.format(save_name))
                cv.imwrite(save_name, img_resized)
                cnt += 1

        self.log_string('>> gen_all_images_src done! \n\n\n')

    def gen_hist_dict(self):
        """
        统计所有images_src的直方图并保存
        :return:
        """
        self.log_string('>> calculating hist ...')
        hist_dict = {}

        for file in os.listdir(self.__DIR_IMAGES_SRC):
            img = cv.imread(os.path.join(self.__DIR_IMAGES_SRC, file))
            hist = []
            for i in range(3):
                ht = cv.calcHist([img], [i], None, [256], [0, 256])
                hist.append(ht)
            hist_dict[file] = hist

        self.log_string('>> calculating hist done ! \n\n\n')
        self.__hist_dict = hist_dict

    def match_replace(self):
        """
        将素材拼成目标图像
        """
        self.log_string(">> matching and replacing ...")
        height, width, channel = self.__TARGET_SHAPE
        image_target = deepcopy(self.__image_target)

        dy, dx = self.__RESIZE_SHAPE_DATASET

        for i in range(0, height, dy):
            for j in range(0, width, dx):
                img = image_target[i:i + dy, j:j + dx, 0:3]

                hist = []
                for k in range(3):
                    ht = cv.calcHist([img], [k], None, [256], [0, 256])
                    hist.append(ht)
                rename = 0
                sim = 0.0
                for key in self.__hist_dict:
                    match0 = cv.compareHist(hist[0], self.__hist_dict[key][0], cv.HISTCMP_CORREL)
                    match1 = cv.compareHist(hist[1], self.__hist_dict[key][1], cv.HISTCMP_CORREL)
                    match2 = cv.compareHist(hist[2], self.__hist_dict[key][2], cv.HISTCMP_CORREL)
                    match = match0 + match1 + match2

                    if match >= sim:
                        sim = match
                        rename = key
                if i + dy <= height and j + dx <= width:
                    image_target[i:i + dy, j:j + dx, 0:3] = cv.imread(os.path.join(self.__DIR_IMAGES_SRC, rename))

        cv.imwrite(os.path.join(self.__DIR_IMAGES, self.__generate_save_name), image_target)
        self.log_string('>> matching and replacing done ! \n\n\n ')

    def mixup(self, weithts):
        """
        将生成的图像与目标图像做mixup,得到更好的效果
        """
        self.log_string('mixing ...')
        image1 = self.__image_target
        image2 = cv.imread(os.path.join(self.__DIR_IMAGES, self.__generate_save_name))
        dst = cv.addWeighted(image1, 1-weithts, image2, weithts, 3)
        cv.imwrite(os.path.join(self.__DIR_IMAGES, self.__mixup_save_name), dst)
        self.log_string('mixing done ! \n\n\n')

    def run(self):
        if self.__is_generate:
            self.gen_all_images_src()
        else:
            assert os.listdir(self.__DIR_IMAGES_SRC), 'image_src_dir is empty!'
        self.gen_hist_dict()
        self.match_replace()
        if self.__is_mixup:
            self.mixup(self.__mixmup_weights)

    def resize_target_image(self):
        if self.__is_resize_target:
            if not self.__image_target.shape == self.__RESIZE_SHAPE_TARGET:
                self.log_string('>> resizing target image ...')
                self.__image_target = cv.resize(self.__image_target, self.__RESIZE_SHAPE_TARGET)
                self.log_string('>> resize done ! \n\n\n')
        self.__TARGET_SHAPE = self.__image_target.shape
