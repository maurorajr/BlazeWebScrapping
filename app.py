from flask import Flask, jsonify, render_template
from scraper import initialize_driver, open_page, perform_initial_clicks, resume_deposits

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('menu.html')

@app.route('/api/total-depositos', methods=['GET'])
def total_depositos():
    try:
        driver = initialize_driver()
        open_page(driver, "https://blaze1.space/pt")
        perform_initial_clicks(driver)
        deposits = resume_deposits(driver, "https://blaze1.space/pt/account/transactions/deposits")
        driver.quit()

        total_amount = sum(d['amount'] for d in deposits if d['status'].lower() == 'complete')
        return jsonify({
            "title": "Total Depósitos",
            "message": f"Total Depósitos Completos: R$ {total_amount:.2f}",
            "details": deposits
        })
    except Exception as e:
        return jsonify({"title": "Erro", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
