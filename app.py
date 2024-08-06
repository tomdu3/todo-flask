from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    """default route

    Returns:
        template: index.html
    """
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
