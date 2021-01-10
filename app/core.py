import os
import shutil
import yaml
from app import app


def create(workspace_dir, data_dir):
    yolov5_dir = app.config['YOLOV5_DIR']
    print('Yolov5安装路径为：{}'.format(yolov5_dir))
    generate_workspace(workspace_dir, yolov5_dir, data_dir)


def run(workspace_dir, data_dir):
    yolov5_dir = app.config['YOLOV5_DIR']
    print('Yolov5安装路径为：{}'.format(yolov5_dir))
    print('项目目录为：{}'.format(workspace_dir))
    print('数据目录为：{}'.format(data_dir))

    train_py_path = os.path.join(yolov5_dir, 'train.py')
    weights = os.path.join(yolov5_dir, 'weights', 'yolov5x.pt')
    cfg = os.path.join(workspace_dir, 'yolov5x.yaml')
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
          f'--device {device}' \
          f'--project {save_dir}'

    print('=================')
    print(cmd)
    print('=================')
    os.system(cmd)


def generate_workspace(workspace_dir, yolov5_dir, data_dir):
    create_data_yaml(workspace_dir, data_dir)
    copy_yolov5_yaml(workspace_dir, yolov5_dir)
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


def copy_yolov5_yaml(workspace_dir, yolov5_dir, yolov5_model='yolov5x'):
    yolov5_model_name = yolov5_model + '.yaml'
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


if __name__ == '__main__':
    copy_yolov5_yaml(r'D:\workspace\yolov5\mask_wearing\20200103', r'D:\github\yolov5')
