import os
import subprocess
from flask import Flask, flash, render_template, request, redirect, url_for

UPLOAD_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "upload")
CLI_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "give-me-the-odds.py")
MILLENNIUM_FALCON_JSON_FILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "millennium-falcon.json")

PERMITTED_EXTENSIONS = {'json'}

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/do_upload', methods=['POST'])
def do_upload():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        # if file and permit_file(file.filename):
        if file:
            empire_json_file_path = os.path.join(
                UPLOAD_FOLDER_PATH, file.filename)
            file.save(empire_json_file_path)
            probability_of_success = execute_cli(empire_json_file_path)
            print("probability of success: ", probability_of_success)
            return render_template("index.html", score=probability_of_success)


def execute_cli(empire_json_file_path):
    print("millennium_falcon_json_file_path", MILLENNIUM_FALCON_JSON_FILE_PATH)
    print("empire_json_file_path", empire_json_file_path)

    command = 'python {} {} {}'.format(CLI_PATH,
                                       MILLENNIUM_FALCON_JSON_FILE_PATH, empire_json_file_path)

    print("command: ", command)
    p = subprocess.Popen(
        [command],
        shell=True,
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    output, error = p.communicate()

    if len(output) < 8:
        result = output.decode("utf-8").split("\n")[-2]+'%'
    else:
        result = output.decode("utf-8").split("\n")
        result = ' '.join(result)

    return result


def permit_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in PERMITTED_EXTENSIONS


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
