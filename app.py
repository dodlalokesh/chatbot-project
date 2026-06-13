from flask import Flask, request, jsonify

app = Flask(__name__)

courses = {
    "aws": "AWS Solutions Architect",
    "devops": "DevOps Master Program",
    "python": "Python Full Course",
    "kubernetes": "Certified Kubernetes Administrator"
}

@app.route("/")
def home():
    return "Chatbot Running Successfully"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message","").lower()

    for key in courses:
        if key in msg:
            return jsonify({"response": courses[key]})

    return jsonify({"response":"Ask about AWS, DevOps, Python or Kubernetes"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
