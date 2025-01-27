from flask import Flask, render_template, request
import pandas as pd
import unicodedata

app = Flask(__name__)

# Încarcă datele despre medicamente
medications_data = pd.read_csv('data/medications.csv', encoding='utf-8', sep=';')

# Funcție pentru eliminarea diacriticelor
def remove_diacritics(text):
    if isinstance(text, str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
    return text

# Aplicăm eliminarea diacriticelor în toate datele
medications_data['Nume Medicament'] = medications_data['Nume Medicament'].apply(remove_diacritics)
medications_data['Substanță Activă'] = medications_data['Substanță Activă'].apply(remove_diacritics)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Preluăm și prelucrăm termenul de căutare
    query = remove_diacritics(request.form['query'].strip().lower())

    # Căutăm doar medicamentele care încep cu termenul introdus
    results = medications_data[
        (medications_data['Nume Medicament'].str.lower().str.startswith(query, na=False)) |
        (medications_data['Substanță Activă'].str.lower().str.startswith(query, na=False))
    ]

    # Verificăm dacă există rezultate
    if results.empty:
        return render_template('results.html', query=query, results=None, message="Elementul nu există!")
    else:
        return render_template('results.html', query=query, results=results.to_dict(orient='records'))

# Endpoint pentru pagina de analize laborator
@app.route('/analize-laborator')
def analize_laborator():
    return render_template('laboratory.html')

# Endpoint pentru pagina de farmacologie
@app.route('/farmacologie')
def farmacologie():
    return render_template('pharmacology.html')

if __name__ == '__main__':
    app.run(debug=True)

# Afișează primele rânduri din fișierul CSV pentru verificare
print(medications_data.head())
