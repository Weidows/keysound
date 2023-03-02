import webview


def testfn(val):
    print("testfn called with value: " + val)
    return "testfn called"

if __name__ == '__main__':
    window = webview.create_window('Test', 'index.html')
    window.expose(testfn)
    webview.start(debug=True)