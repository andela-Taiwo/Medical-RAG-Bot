from flask import Flask, render_template, request, session, redirect, url_for
from app.config.settings import DB_FAISS_PATH
from app.rag_system import vector_store
from app.rag_system.retriever import create_qa_chain
from dotenv import load_dotenv
from app.rag_system import data_loader
import os

from markupsafe import Markup

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)


def nl2br(value):
    return Markup(value.replace("\n", "<br>"))


app.jinja_env.filters["nl2br"] = nl2br


@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt")

        if user_input:
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})
            session["messages"] = messages

            try:
                qa_chain = create_qa_chain()
                if qa_chain is None:
                    raise Exception("QA chain not created")
                response = qa_chain.invoke({"query": user_input})
                result = response.get("result", "No response")

                messages.append({"role": "assistant", "content": result})
                session["messages"] = messages
            except Exception as e:
                error_msg = f"Error : {str(e)}"
                return render_template(
                    "index.html", messages=session["messages"], error=error_msg
                )
        return redirect(url_for("index"))
    return render_template("index.html", messages=session.get("messages", []))


@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Build data pipeline
    data_loader.process_and_store_pdfs()
    app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)
