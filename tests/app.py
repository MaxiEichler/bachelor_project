from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simple HTML template (embedded for demo)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask GUI Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        .container { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
        input, button { width: 100%; padding: 10px; margin-top: 10px; }
        h2 { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Flask GUI Demo</h2>
        <form method="post" action="/">
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name" placeholder="Your name" required>
            <button type="submit">Say Hello</button>
        </form>
        {% if name %}
        <h3>Hello, {{ name }} 👋</h3>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    name = None
    if request.method == "POST":
        name = request.form.get("name")
    return render_template_string(HTML_PAGE, name=name)

if __name__ == "__main__":
    app.run(debug=True)
