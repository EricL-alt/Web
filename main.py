@app.route('/<string:hostname>/<string:username>/<string:password>/<path:remote_script_path>')
def hello(hostname,username,password,remote_script_path):
    print(hostname)
    print(username)
    print(password)
    print(str(remote_script_path))

@app.route('/ok')
def ok():
    print("hello world")
    return(" ")
if __name__ == '__main__':
    app.run(debug=True)
