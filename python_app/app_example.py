from flask.helpers import url_for
import pyexcel_xlsx as pe
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import send_from_directory
import cert_gen
import re

raw_data = pe.get_data(r'./data.xlsx')
countries = list(raw_data.keys())
users = []
users_json = []
server_path = 'server_name:5000'
server_ip = ''
upload_folder = ''


def date_convert(dt):
    return '.'.join(dt.split('-')[::-1])

def replace_space(word):
      return re.sub('\s$', '', word)

for country in countries:
    users.extend(list(filter(lambda x: len(x) > 0, raw_data[country][1:])))
#   print(users[1])

def get_code(last_name, first_name, middle_name, birth_date):
    print(last_name, first_name, middle_name, date_convert(birth_date))
    result = list(
        filter(lambda x: x[2].lower() == '{} {} {}'.format(replace_space(last_name.lower()), replace_space(first_name.lower()), replace_space(middle_name.lower())) \
             and x[6] == date_convert(birth_date), users)) \
            if len(middle_name) > 0 else \
                list(
        filter(lambda x: x[2].lower() == '{} {}'.format(replace_space(last_name.lower()), replace_space(first_name.lower())) \
             and x[6] == date_convert(birth_date), users))

    return result[0][8:10] if len(result) > 0 else 'User not found'



# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = upload_folder
# enable CORS
CORS(app)

@app.route('/certs', methods=['GET', 'POST'])
@cross_origin()
def certs():
    response_object = {}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        last_name_users = post_data.get('last_name')
        first_name_user = post_data.get('first_name')
        middle_name_user = post_data.get('middle_name')
        birth_date_user = post_data.get('birth_date')

        response_object['message'] = get_code(
            last_name_users, first_name_user, middle_name_user, birth_date_user)
        print(response_object)
        if response_object['message'] != 'User not found':
            file_names = cert_gen.generate_cert(response_object['message'])
            response_object['links'] =['http://{}/uploads/{}.pdf'.format(server_path, file_name) for file_name in file_names]
            response_object['showMessage'] = True
            print(response_object)
            return jsonify(response_object)
        response_object['error'] = True
        response_object['showMessage'] = False
        return jsonify(response_object)
    else:
        response_object['status'] = 'Failed'
    return jsonify(response_object)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = app.config['UPLOAD_FOLDER']
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host=server_ip')
