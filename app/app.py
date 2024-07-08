from flask import Flask, request, jsonify, send_file
from utils.utility import auth, get_file_path, find_file_by_hash

import os
import hashlib


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    '''
    Загружает файл на сервер.

    Возвращает:
        JSON: {'file_hash': '<file_hash>'} в случае успешной загрузки,
        HTTP 400 с сообщением об ошибке в противном случае.
    '''

    if 'file' not in request.files:
        return jsonify({'error': 'Файл не загружен'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не добавлен'}), 400

    file_content = file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    _, file_extension = os.path.splitext(file.filename)
    file_path = get_file_path(file_hash, file_extension)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    return jsonify({'file_hash': file_hash}), 201


@app.route('/download/<file_hash>', methods=['GET'])
def download_file(file_hash):
    '''
    Скачивает файл с сервера.

    Аргументы:
        file_hash (str): Хэш файла для скачивания.

    Возвращает:
        File: Запрашиваемый файл как вложение, или JSON сообщение об
        ошибке, если файл не найден.
    '''
    file_path = find_file_by_hash(file_hash)
    if file_path:
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'Файл не найден'}), 404


@app.route('/delete/<file_hash>', methods=['DELETE'])
@auth.login_required
def delete_file(file_hash):
    '''
    Удаляет файл с сервера.

    Аргументы:
        file_hash (str): Хэш файла для удаления.

    Возвращает:
        JSON: {'message': 'Файл удален'} в случае успешного удаления, или
        JSON сообщение об ошибке, если файл не найден.
    '''
    file_path = find_file_by_hash(file_hash)
    if file_path:
        os.remove(file_path)
        return jsonify({'message': 'Файл удален'}), 200
    return jsonify({'error': 'Файл не найден'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
