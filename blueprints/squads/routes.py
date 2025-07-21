from . import squads_bp
from flask import render_template, request, redirect, url_for, flash
from utils.sheets import get_squads, add_squad, update_squad, delete_squad, get_times

# ✅ Rota principal Squads
@squads_bp.route('/squads-ui', methods=['GET', 'POST'])
def cadastro_squads():
    if request.method == 'POST':
        nome = request.form['nome']
        time = request.form['time']
        if nome and time:
            add_squad(nome, time)
            flash('Squad cadastrado com sucesso!', 'success')
        else:
            flash('Preencha todos os campos.', 'danger')
        return redirect(url_for('squads.cadastro_squads'))

    squads = get_squads()
    times = get_times()
    squads_sorted = sorted(squads, key=lambda x: x['Nome'])
    return render_template('squads_cadastro.html', squads=squads_sorted, times=times)

# ✅ Rota editar Squad
@squads_bp.route('/editar-squad/<int:id>', methods=['GET', 'POST'])
def editar_squad(id):
    if request.method == 'POST':
        nome = request.form['nome']
        time = request.form['time']
        update_squad(id, nome, time)
        flash('Squad atualizado com sucesso!', 'success')
        return redirect(url_for('squads.cadastro_squads'))
    return redirect(url_for('squads.cadastro_squads'))

# ✅ Rota remover Squad
@squads_bp.route('/remover-squad/<int:id>', methods=['POST'])
def remover_squad(id):
    delete_squad(id)
    flash('Squad removido com sucesso!', 'success')
    return redirect(url_for('squads.cadastro_squads'))
