import configparser
from flask import Flask, render_template, request, send_file
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_attachment(recipient_email, subject, body, pdf_file_path):
    parser = configparser.ConfigParser()
    with open('config.ini', mode='r') as file:
        parser.read_file(file)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = parser['login']['email']
    smtp_password = parser['login']['password']

    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with open(pdf_file_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    attach.add_header("Content-Disposition",f"attachment; filename=topsis_results.pdf")
    with open("temp.csv", 'rb') as file:
        attach1 = MIMEApplication(file.read(), _subtype="csv")
    attach1.add_header("Content-Disposition",f"attachment; filename=input.csv")
    message.attach(attach)
    message.attach(attach1)

    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(smtp_username, recipient_email, message.as_string())
        smtp_connection.quit()
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False


app = Flask(__name__)


def create_pdf_report(ranked_alternatives):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "TOPSIS Results")
    y = 780
    for alt, rank in ranked_alternatives.items():
        c.drawString(100, y, f"{alt}: Rank {rank}")
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer


def topsis(input_file, weights):
    data = pd.read_csv(input_file)
    alternatives = data.iloc[:, 0].tolist()
    criteria = data.columns[1:].tolist()
    X = data[criteria].values

    normalized_matrix = X / np.sqrt(np.sum(X ** 2, axis=0))

    if len(weights) != normalized_matrix.shape[1]:
        raise ValueError(
            "Number of weights should match the number of criteria in the decision matrix.")

    weighted_matrix = normalized_matrix * np.array(weights)

    ideal_best = np.max(weighted_matrix, axis=0)
    ideal_worst = np.min(weighted_matrix, axis=0)

    dist_to_ideal_best = np.sqrt(
        np.sum((weighted_matrix - ideal_best) ** 2, axis=1))
    dist_to_ideal_worst = np.sqrt(
        np.sum((weighted_matrix - ideal_worst) ** 2, axis=1))

    topsis_scores = dist_to_ideal_worst / \
        (dist_to_ideal_best + dist_to_ideal_worst)

    ranks = pd.Series(topsis_scores, index=alternatives).rank(ascending=False)

    ranked_alternatives = ranks.sort_values()

    return ranked_alternatives


@app.route("/", methods=["GET", "POST"])
def topsis_web():
    if request.method == "POST":
        try:
            file = request.files["file"]
            file_path = "temp.csv"
            file.save(file_path)

            data = pd.read_csv(file_path)
            criteria = data.columns[1:].tolist()

            num_criteria = len(criteria)
            weights = [float(request.form.get(
                f"weight{i}")) for i in range(num_criteria)]

            ranked_alternatives = topsis(file_path, weights)

            pdf_report_buffer = create_pdf_report(ranked_alternatives)
            pdf_file_path = "temp_report.pdf"
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(pdf_report_buffer.getvalue())

            subject = "TOPSIS Results"
            body = "Ranking of Alternates are attached with email"

            return render_template("result.html", ranked_alternatives=ranked_alternatives, pdf_file_path=pdf_file_path, subject=subject, body=body)
        except Exception as e:
            error_message = str(e)
            return render_template("error.html", error=error_message)
    else:
        return render_template("index.html", num_criteria=3, criteria=[])


@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        recipient_email = request.form["email"]
        pdf_file_path = request.form["pdf_report"]
        subject = request.form["subject"]
        body = request.form["body"]

        email_sent = send_email_with_attachment(
            recipient_email, subject, body, pdf_file_path)

        return render_template("email_status.html", email_sent=email_sent)
    except Exception as e:
        error_message = str(e)
        return render_template("error.html", error=error_message)


if __name__ == "__main__":
    app.run(debug=True)
