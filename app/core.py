import os
import sys
import shutil
import yaml
from app import app


def create(workspace_dir, data_dir, model_select=3):
    yolov5_dir = app.config['YOLOV5_DIR']
    print('Yolov5安装路径为：{}'.format(yolov5_dir))
    generate_workspace(workspace_dir, yolov5_dir, data_dir, model_select)


def generate_workspace(workspace_dir, yolov5_dir, data_dir, model_select):
    create_data_yaml(workspace_dir, data_dir)
    copy_yolov5_yaml(workspace_dir, yolov5_dir, model_select)
    copy_hyp_finetune_yaml(workspace_dir, yolov5_dir)


def create_data_yaml(workspace_dir, data_dir):
    data_yaml_src_path = os.path.join(data_dir, 'data.yaml')
    data_yaml_dst_path = os.path.join(workspace_dir, 'data.yaml')
    shutil.copy(data_yaml_src_path, data_yaml_dst_path)

    train_dir = os.path.join(data_dir, 'train/images')
    val_dir = os.path.join(data_dir, 'valid/images')

    with open(data_yaml_dst_path, 'r', encoding='utf-8') as f:
        yaml.warnings({'YAMLLoadWarning': False})
        data_yaml_dict = yaml.load(f)

    with open(data_yaml_dst_path, 'w', encoding='utf-8') as f:
        data_yaml_dict['train'] = train_dir
        data_yaml_dict['val'] = val_dir
        yaml.dump(data_yaml_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def copy_yolov5_yaml(workspace_dir, yolov5_dir, model_select):
    model_dict = {
        1: 'yolov5s',
        2: 'yolov5m',
        3: 'yolov5l',
        4: 'yolov5x',
    }
    selected_model = model_dict.get(model_select, 3)
    yolov5_model_name = f'{selected_model}.yaml'
    yolov5_yaml_src_path = os.path.join(yolov5_dir, 'models', yolov5_model_name)
    yolov5_yaml_dst_path = os.path.join(workspace_dir, yolov5_model_name)
    shutil.copy(yolov5_yaml_src_path, yolov5_yaml_dst_path)

    data_yaml_path = os.path.join(workspace_dir, 'data.yaml')
    with open(data_yaml_path, 'r', encoding='utf-8') as f:
        yaml.warnings({'YAMLLoadWarning': False})
        data_yaml_dict = yaml.load(f)
        nc = data_yaml_dict['nc']

    with open(yolov5_yaml_dst_path, 'r', encoding='utf-8') as f:
        yolov5_yaml_dict = yaml.load(f)

    yolov5_yaml_dict['nc'] = nc

    with open(yolov5_yaml_dst_path, 'w', encoding='utf-8') as f:
        yaml.dump(yolov5_yaml_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def copy_hyp_finetune_yaml(workspace_dir, yolov5_dir):
    hyp_finetune_yaml_src_path = os.path.join(yolov5_dir, 'data', 'hyp.finetune.yaml')
    hyp_finetune_yaml_dst_path = os.path.join(workspace_dir, 'hyp.finetune.yaml')
    shutil.copy(hyp_finetune_yaml_src_path, hyp_finetune_yaml_dst_path)


def train(workspace_dir, data_dir, model_select=3):
    yolov5_dir = app.config['YOLOV5_DIR']
    print('Yolov5安装路径为：{}'.format(yolov5_dir))
    print('项目目录为：{}'.format(workspace_dir))
    print('数据目录为：{}'.format(data_dir))
    train_py_path = os.path.join(yolov5_dir, 'train.py')

    model_dict = {
        1: 'yolov5s',
        2: 'yolov5m',
        3: 'yolov5l',
        4: 'yolov5x',
    }
    selected_model = model_dict.get(model_select, 3)
    print(f'选择的模型是{selected_model}')

    weights = os.path.join(yolov5_dir, 'weights', f'{selected_model}.pt')
    cfg = os.path.join(workspace_dir, f'{selected_model}.yaml')
    data = os.path.join(workspace_dir, 'data.yaml')
    hyp = os.path.join(workspace_dir, 'hyp.finetune.yaml')
    batch_size = '4'
    device = '0'
    save_dir = os.path.join(workspace_dir, 'runs/train')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cmd = f'python {train_py_path} ' \
          f'--weights {weights} ' \
          f'--cfg {cfg} ' \
          f'--data {data} ' \
          f'--hyp {hyp} ' \
          f'--batch-size {batch_size} ' \
          f'--device {device} ' \
          f'--project {save_dir}'
    print('=================')
    print(cmd)
    print('=================')
    os.chdir(yolov5_dir)
    os.system(cmd)


def test(workspace_dir):
    yolov5_dir = app.config['YOLOV5_DIR']
    test_py_path = os.path.join(yolov5_dir, 'test.py')
    weights = os.path.join(workspace_dir, 'runs', 'train', 'exp', 'weights', 'best.pt')
    data = os.path.join(workspace_dir, 'data.yaml')
    conf_thres = 0.6
    iou_thres = 0.65
    device = '0'
    save_dir = os.path.join(workspace_dir, 'runs/test')

    cmd = f'python {test_py_path} ' \
          f'--weights {weights} ' \
          f'--data {data} ' \
          f'--conf-thres {conf_thres} ' \
          f'--iou-thres {iou_thres} ' \
          f'--device {device} ' \
          f'--verbose ' \
          f'--save-txt ' \
          f'--save-hybrid ' \
          f'--save-conf ' \
          f'--project {save_dir}'
    print('=================')
    print(cmd)
    print('=================')
    os.chdir(yolov5_dir)
    os.system(cmd)


def detect(workspace_dir, data_dir):
    yolov5_dir = app.config['YOLOV5_DIR']
    detect_py_path = os.path.join(yolov5_dir, 'detect.py')
    weights = os.path.join(workspace_dir, 'runs', 'train', 'exp', 'weights', 'best.pt')
    detect_dir = os.path.join(data_dir, 'test', 'images')
    source = os.path.join(detect_dir, '*.jpg')
    conf_thres = 0.6
    iou_thres = 0.6
    device = '0'
    save_dir = os.path.join(workspace_dir, 'runs/detect')

    cmd = f'python {detect_py_path} ' \
          f'--weights {weights} ' \
          f'--source {source} ' \
          f'--conf-thres {conf_thres} ' \
          f'--iou-thres {iou_thres} ' \
          f'--device {device} ' \
          f'--view-img ' \
          f'--save-txt ' \
          f'--save-conf ' \
          f'--project {save_dir}'
    print('=================')
    print(cmd)
    print('=================')
    os.chdir(yolov5_dir)
    os.system(cmd)
