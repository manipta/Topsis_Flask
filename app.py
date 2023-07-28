from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64


def send_email_with_attachment(recipient_email, subject, body, pdf_file_path):
    # Set up the SMTP server (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "prdct4u@gmail.com"  # Replace with your Gmail email address
    smtp_password = "Mani123."   # Replace with your Gmail email password

    # Create a MIMEText object to represent the email body
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach the PDF to the email
    with open("temp_report.pdf", "rb") as f:
        attach = MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header("Content-Disposition", f"attachment; filename=topsis_results.pdf")
    # attachment1 = MIMEText(file.getvalue(),"csv")
    # attachment1.add_header("Content-Disposition", f"attachment; filename=input.csv")
    message.attach(attach)
    # message.attach(attachment1)

    # Send the email using SMTP
    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(smtp_username, recipient_email, message.as_string())
        smtp_connection.quit()
        return True  # Email sent successfully
    except Exception as e:
        print("Error sending email:", str(e))
        return False  # Failed to send email

app = Flask(__name__)
def create_pdf_report(ranked_alternatives):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set up the PDF content
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
        # Load the decision matrix from the CSV file
        data = pd.read_csv(input_file)

        # Extract the alternative names and criterion names
        alternatives = data.iloc[:, 0].tolist()
        criteria = data.columns[1:].tolist()  # Update this line to include all criteria columns

        # Extract the decision matrix values by selecting only the criterion columns
        X = data[criteria].values

        # Step 1: Normalize the decision matrix
        normalized_matrix = X / np.sqrt(np.sum(X ** 2, axis=0))

        # Step 2: Check if the dimensions of the weights match the number of criteria
        if len(weights) != normalized_matrix.shape[1]:
            raise ValueError("Number of weights should match the number of criteria in the decision matrix.")

        # Step 3: Multiply the normalized matrix by the weight values
        weighted_matrix = normalized_matrix * np.array(weights)

        # Step 4: Identify the ideal and negative-ideal solutions
        ideal_best = np.max(weighted_matrix, axis=0)
        ideal_worst = np.min(weighted_matrix, axis=0)

        # Step 5: Calculate the Euclidean distances to the ideal and negative-ideal solutions
        dist_to_ideal_best = np.sqrt(np.sum((weighted_matrix - ideal_best) ** 2, axis=1))
        dist_to_ideal_worst = np.sqrt(np.sum((weighted_matrix - ideal_worst) ** 2, axis=1))

        # Step 6: Calculate the relative closeness to the ideal solution
        topsis_scores = dist_to_ideal_worst / (dist_to_ideal_best + dist_to_ideal_worst)

        # Step 7: Rank the alternatives based on their TOPSIS scores
        ranks = pd.Series(topsis_scores, index=alternatives).rank(ascending=False)

        # Step 8: Sort the alternatives based on their ranks
        ranked_alternatives = ranks.sort_values()

        return ranked_alternatives
@app.route("/", methods=["GET", "POST"])
def topsis_web():
    if request.method == "POST":
        try:
            # Get the uploaded CSV file
            file = request.files["file"]

            # Save the uploaded file to a temporary location
            file_path = "temp.csv"
            file.save(file_path)

            # Load the criteria from the CSV file (first row, excluding the first column)
            data = pd.read_csv(file_path)
            criteria = data.columns[1:].tolist()

            # Get the criterion weights from the form
            num_criteria = len(criteria)
            weights = [float(request.form.get(f"weight{i}")) for i in range(num_criteria)]

            # Perform TOPSIS and get ranked alternatives
            ranked_alternatives = topsis(file_path, weights)
            
            # pdf_report = create_pdf_report(ranked_alternatives)
            pdf_report_buffer = create_pdf_report(ranked_alternatives)
            pdf_file_path = "temp_report.pdf"
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(pdf_report_buffer.getvalue())
            # Get the base64-encoded PDF content
            # pdf_report_base64 = base64.b64encode(pdf_report_buffer).decode()
            # Remove the temporary file
            import os
            os.remove(file_path)
            # os.remove(pdf_file_path)
            subject = "TOPSIS Results"
            body = "Ranked Alternates are attached with email"
            
            return render_template("result.html", ranked_alternatives=ranked_alternatives, pdf_file_path=pdf_file_path, subject=subject, body=body)
        except Exception as e:
            error_message = str(e)
            return render_template("error.html", error=error_message)
    else:
        # For initial load, return the form with empty criteria list
        return render_template("index.html", num_criteria=3, criteria=[])

@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        # Get the email address and other data from the form
        recipient_email = request.form["email"]
        print("done")
        pdf_file_path = request.form["pdf_report"]
        # csv = BytesIO(request.form["file"])
        print("done")
        subject = request.form["subject"]
        body = request.form["body"]

        # Attach the PDF to the email
        email_sent = send_email_with_attachment(recipient_email, subject, body, pdf_file_path)

        # Show the results page with the email sending status
        return render_template("email_status.html", email_sent=email_sent)
    except Exception as e:
        error_message = str(e)
        return render_template("error.html", error=error_message)

if __name__ == "__main__":
    app.run(debug=True)