from app import app
from flask import render_template
from app.forms import InputForm
from app import core


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        workspace_dir = form.workspace_dir.data
        data_dir = form.data_dir.data
        model_select = form.model_select.data
        if form.create.data:
            core.create(workspace_dir, data_dir, model_select)
        elif form.train.data:
            core.train(workspace_dir, data_dir, model_select)
        elif form.test.data:
            core.test(workspace_dir)
        elif form.detect.data:
            core.detect(workspace_dir, data_dir)

    return render_template('index.html', form=form)
