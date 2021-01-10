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
        if form.create.data:
            core.create(workspace_dir, data_dir)
        elif form.run.data:
            core.run(workspace_dir, data_dir)

    return render_template('index.html', form=form)
