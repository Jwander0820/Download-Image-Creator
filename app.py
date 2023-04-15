from flask import Flask, request, render_template, redirect, url_for, flash

from image_crawler import ImageCrawler

app = Flask(__name__)
app.secret_key = '123456789'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    return "I am OK"


@app.route('/api/download', methods=['POST'])
def api_download():
    input_value = request.form['input_value']
    if input_value.startswith("http"):
        url = input_value
    else:
        token = input_value
        url = f"https://www.bing.com/images/create/a-mystical-interstellar-creature2c-shaped-by-cluste/{token}?FORM=GUH2CR"

    crawler = ImageCrawler(url)
    result_text = crawler.run()
    flash(result_text)
    flash(f"Prompt：{crawler.img_prompt}")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
