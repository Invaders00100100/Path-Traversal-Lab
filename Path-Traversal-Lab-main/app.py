from flask import Flask, request, send_file, render_template_string, abort
import os

app = Flask(__name__)

# HTML template to list and link images
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NFT Gallery</title>
    <style>
        /* Full screen styles */
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #121212;
            color: #FF69B4;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        h1 {
            margin-top: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
        }
        a {
            color: #FF69B4;
        }
        .nft-image {
            max-width: 90%; /* Adjust max-width as needed */
            height: auto;
            margin-bottom: 20px;
        }
        .vulnerability-text {
            color: lime;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>NFT Gallery</h1>
    
    <p class="vulnerability-text">This website is vulnerable to path traversal. See if you can find a way to gain unauthorized access to the forbidden file in the higher level Directory named SECRETS.txt</p>

    <img src="https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/advisor/in/wp-content/uploads/2022/03/monkey-g412399084_1280.jpg" alt="NFT Image" class="nft-image">

    <ul>
    {% for image in images %}
        <li><a href="{{ url_for('download', file=image) }}">{{ image }}</a></li>
    {% endfor %}
    </ul>
    
    {% if message %}
    <p>{{ message }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    base_directory = '/Users/universal/Desktop/Path-Traversal-Lab/images'  # Change this to the directory where images are stored
    try:
        images = os.listdir(base_directory)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, message=f"Error: {str(e)}", images=[])
    return render_template_string(HTML_TEMPLATE, images=images)

@app.route('/download', methods=['GET'])
def download():
    filename = request.args.get('file')
    if not filename:
        abort(400, "File parameter is missing")
    
    base_directory = '/Users/universal/Desktop/Path-Traversal-Lab/images'  # Change this to the directory where images are stored
    file_path = os.path.join(base_directory, filename)
    
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path)
        else:
            abort(404, "File not found")
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, message=f"Error: {str(e)}", images=[])

if __name__ == '__main__':
    app.run(debug=True)
