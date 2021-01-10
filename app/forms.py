import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class InputForm(FlaskForm):
    workspace_dir = StringField('项目目录', validators=[DataRequired()])
    data_dir = StringField('数据目录', validators=[DataRequired()])
    create = SubmitField('Create Workspace')
    run = SubmitField('Start Training')

    def validate_workspace_dir(self, workspace_dir):
        if not os.path.isdir(workspace_dir.data):
            raise ValidationError('工作目录路径不存在。')

    def validate_data_dir(self, data_dir):
        if not os.path.isdir(data_dir.data):
            raise ValidationError('工作目录路径不存在。')
        if not os.path.exists(os.path.join(data_dir.data, 'data.yaml')):
            raise ValidationError('配置文件data.yaml不存在。')
