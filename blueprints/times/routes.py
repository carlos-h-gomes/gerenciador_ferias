from . import times_bp
from flask import render_template, request, redirect, url_for, flash
from utils.sheets import get_times, add_time, update_time, delete_time
import random

# 🔧 Função para gerar cor aleatória em HEX
def gerar_cor_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# ✅ Rota principal Times
@times_bp.route('/times-ui', methods=['GET', 'POST'])
def cadastro_times():
    if request.method == 'POST':
        nome = request.form['nome']
        gestor = request.form['gestor']
        cor = gerar_cor_hex()  # 🔧 gera cor ao cadastrar

        if nome and gestor:
            add_time(nome, gestor, cor)  # 🔧 passa cor ao adicionar
            flash('Time cadastrado com sucesso!', 'success')
        else:
            flash('Preencha todos os campos.', 'danger')
        return redirect(url_for('times.cadastro_times'))

    times = get_times()
    # 🔧 Ordenação backend por Nome do Time
    times_sorted = sorted(times, key=lambda x: x['Nome'])
    return render_template('times_cadastro.html', times=times_sorted)

# ✅ Rota editar Time
@times_bp.route('/editar-time/<int:id>', methods=['GET', 'POST'])
def editar_time(id):
    if request.method == 'POST':
        nome = request.form['nome']
        gestor = request.form['gestor']
        update_time(id, nome, gestor)
        flash('Time atualizado com sucesso!', 'success')
        return redirect(url_for('times.cadastro_times'))
    return redirect(url_for('times.cadastro_times'))

# ✅ Rota remover Time
@times_bp.route('/remover-time/<int:id>', methods=['POST'])
def remover_time(id):
    delete_time(id)
    flash('Time removido com sucesso!', 'success')
    return redirect(url_for('times.cadastro_times'))
