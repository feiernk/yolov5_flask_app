import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError


class InputForm(FlaskForm):
    workspace_dir = StringField('项目目录', validators=[DataRequired()])
    data_dir = StringField('数据目录', validators=[DataRequired()])

    model_select = SelectField(
        label='模型选择',
        validators=[DataRequired('请选择模型')],
        render_kw={
            'class': 'form-control'
        },
        choices=[
            (1, 'YOLOv5s'),
            (2, 'YOLOv5m'),
            (3, 'YOLOv5l'),
            (4, 'YOLOv5x')
        ],
        default=3,
        coerce=int
    )

    create = SubmitField('Create Workspace')
    train = SubmitField('Start Training')  # 训练
    test = SubmitField('Start Testing')  # 测试
    detect = SubmitField('Start Detecting')  # 推理

    def validate_workspace_dir(self, workspace_dir):
        if not os.path.isdir(workspace_dir.data):
            raise ValidationError('工作目录路径不存在。')

    def validate_data_dir(self, data_dir):
        if not os.path.isdir(data_dir.data):
            raise ValidationError('工作目录路径不存在。')
        if not os.path.exists(os.path.join(data_dir.data, 'data.yaml')):
            raise ValidationError('配置文件data.yaml不存在。')
