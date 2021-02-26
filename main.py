# -*- encoding: utf-8 -*-

# Author:   Hengyu Jiang
# Time:     2021/2/14 14:37
# Email:    hengyujiang.njust.edu.cn
# Project:  MontageTransform
# File:     main.py
# Product:  PyCharm
# Desc:     

import argparse
from utils.MontageChanger import MonTageTransformer

parser = argparse.ArgumentParser()
parser.add_argument('--target_image', help='path to the target image')
parser.add_argument('--dataset', help='dir in which the image datast is restored')
parser.add_argument('--dir_src', default='./images/image_src/',
                    help='dir in which the generated component images to save. [default: ./images/images_src/]')
parser.add_argument('--dir_log', default='./log/', help='Log dir [default: ./log/]')
parser.add_argument('--dir_images', default='./images/',
                    help='dir in which the generated images to save [default: ./images]')
parser.add_argument('--dataset_reshape', help='the shape the component images will be reshaped into')
parser.add_argument('--is_generate', action='store_true', help='if generate component images from dataset [default: True]')
parser.add_argument('--is_resize_target', action='store_true', help='if resize the target image [default: True]')
parser.add_argument('--target_reshape', default=str((1080,1440)),
                    help='the shape the target image will be reshaped into [default: (1080, 1440)]')
parser.add_argument('--is_mixup', action='store_true', help='if mix the target image and the generated image [default: True]')
parser.add_argument('--mixup_weights', type=float, default=0.8,
                    help='the weight of the generated image in the mixup operation [default: 0.8]')
parser.add_argument('--generate_name', default='generate.jpg',
                    help='save name of the generate image [default: generate.jpg]')
parser.add_argument('--mixup_name', default='mixup.jpg',
                    help='save name of the mixup image [default: mixup.jpg]')
args = parser.parse_args()


path_image_target = args.target_image
dir_images = args.dir_images
is_mixup = args.is_mixup
is_resize_target = args.is_resize_target
is_generate = args.is_generate
dir_log = args.dir_log
generate_save_name = args.generate_name

if is_generate:
	dir_dataset = args.dataset
	resize_shape_dataset = tuple(eval(args.dataset_reshape))
	dir_images_src = args.dir_src
else:
	dir_dataset = None
	resize_shape_dataset = None
	dir_images_src = None

if is_resize_target:
	resize_shape_target = tuple(eval(args.target_reshape))
else:
	resize_shape_target = None

if is_mixup:
	mixup_save_name = args.mixup_name
	mixup_weights = args.mixup_weights
else:
	mixup_weights = 0
	mixup_save_name = None


transformer = MonTageTransformer(path_image_target=path_image_target, resize_shape_target=resize_shape_target,
                                 resize_shape_dataset=resize_shape_dataset, dir_images=dir_images, dir_images_src=dir_images_src,
                                 dir_dataset=dir_dataset, dir_log=dir_log, generate_save_name=generate_save_name,
                                 mixup_save_name=mixup_save_name, mixup_weights=mixup_weights, is_mixup=is_mixup,
                                 is_resize_target=is_resize_target, is_generate=is_generate)
transformer.run()
