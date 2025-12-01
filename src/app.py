from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto


app = Flask(__name__)


class WarehouseStore:
    def __init__(self):
        self.warehouses = {}
        self.next_id = 1

    def get_next_id(self):
        current_id = self.next_id
        self.next_id += 1
        return current_id

    def add(self, name, varasto):
        warehouse_id = self.get_next_id()
        self.warehouses[warehouse_id] = {'name': name, 'varasto': varasto}
        return warehouse_id

    def get(self, warehouse_id):
        return self.warehouses.get(warehouse_id)

    def delete(self, warehouse_id):
        if warehouse_id in self.warehouses:
            del self.warehouses[warehouse_id]

    def all(self):
        return self.warehouses


store = WarehouseStore()


@app.route('/')
def index():
    return render_template('index.html', warehouses=store.all())


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            capacity = float(request.form.get('capacity', 0))
            initial = float(request.form.get('initial', 0))
        except ValueError:
            return render_template(
                'create.html',
                error='Invalid number format'
            )

        if not name:
            return render_template('create.html', error='Name is required')

        store.add(name, Varasto(capacity, initial))
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    warehouse = store.get(warehouse_id)
    if warehouse is None:
        return redirect(url_for('index'))
    return render_template(
        'view.html',
        warehouse_id=warehouse_id,
        warehouse=warehouse
    )


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    warehouse = store.get(warehouse_id)
    if warehouse is None:
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    warehouse['varasto'].lisaa_varastoon(amount)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    warehouse = store.get(warehouse_id)
    if warehouse is None:
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    warehouse['varasto'].ota_varastosta(amount)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    warehouse = store.get(warehouse_id)
    if warehouse is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            warehouse['name'] = name
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    return render_template(
        'edit.html',
        warehouse_id=warehouse_id,
        warehouse=warehouse
    )


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    store.delete(warehouse_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
