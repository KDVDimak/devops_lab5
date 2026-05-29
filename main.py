# Модель: Обчислення значення функції та оцінка похибок (5 семестр)
# Автор: Кривонос Дмитро, група АІ-231


from flask import Flask, request, jsonify

import os

app = Flask(__name__)


def calculate_model(a, Da, b, Db, c, Dc):
    # Обчислення функції
    f = (a * c) / (a - b ** 2)

    # Похибка за правилами арифметичних операцій
    rel_ac = Da / a + Dc / c
    delta_b2 = 2 * b * Db
    delta_d = Da + delta_b2
    rel_d = delta_d / abs(a - b ** 2)

    rel_f = rel_ac + rel_d
    df_rules = abs(f) * rel_f

    # Похибка за загальною формулою
    df_da = -(c * b ** 2) / (a - b ** 2) ** 2
    df_db = (2 * a * b * c) / (a - b ** 2) ** 2
    df_dc = a / (a - b ** 2)

    df_formula = abs(df_da) * Da + abs(df_db) * Db + abs(df_dc) * Dc

    return {
        "a": a,
        "Da": Da,
        "b": b,
        "Db": Db,
        "c": c,
        "Dc": Dc,
        "f": round(f, 5),
        "delta_f_rules": round(df_rules, 5),
        "delta_f_formula": round(df_formula, 5),
        "result": f"{f:.2f} ± {df_rules:.2f}"
    }


@app.route('/calculate', methods=['GET'])
def calculate():
    try:
        a = float(request.args.get('a', 16.5))
        Da = float(request.args.get('Da', 0.05))
        b = float(request.args.get('b', 4.12))
        Db = float(request.args.get('Db', 0.005))
        c = float(request.args.get('c', 0.198))
        Dc = float(request.args.get('Dc', 0.0005))

        result = calculate_model(a, Da, b, Db, c, Dc)

        return jsonify(result)

    except ValueError:
        return jsonify({
            "error": "Усі параметри повинні бути числами"
        }), 400

    except ZeroDivisionError:
        return jsonify({
            "error": "a - b^2 не повинно дорівнювати 0"
        }), 400

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port, debug=False)