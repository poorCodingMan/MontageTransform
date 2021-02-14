# author

- email: 996.icu.icu@gmail.com
- csdn blog: [https://blog.csdn.net/weixin_43848827](https://blog.csdn.net/weixin_43848827)

# introduction

this project generates a montage image from the target image and the image dataset.

# install

`pip install install.txt`

# use

use `python3`, run

```sql
python main.py --target_image ${path to target image} --dataset ${dir in which the dataset images are stored} --dataset_reshape ${the new shape in which the datast images will be reshaped into, for example, (20,20)} --mixup_weights ${the weight of the generated image in the mixup operation} --is_resize_target --is_mixup --is_generate

```

you will see the generated images in `./images/`

# all optional args

```python
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
```

