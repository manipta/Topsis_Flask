# TOPSIS Web Application(Flask)

This is a web application that implements the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) method to rank alternatives based on multiple criteria.

It is currently live at [pythonanywhere](http://manipta.pythonanywhere.com/)

## Description

TOPSIS is a decision-making method used to evaluate and rank alternatives when there are multiple criteria involved. This web application allows users to upload a CSV file containing the decision matrix and specify weights for each criterion. It then calculates the relative closeness to the ideal solution for each alternative and ranks them accordingly.

## Unique Features

- Asking Required Number of Weights (Dynamically)
- Negative Weights can also be handled
- Result Pdf will be genrated
- Sending Email option is also available 

## Details about Features

- Upload CSV file: Users can upload a CSV file containing the decision matrix. The first column should contain the alternative names, and the rest of the columns should represent the criteria.

- Number of Weights: Dynamically Adding Number of Weights from user input.

- Enter Weights: Users can enter weights for each criterion using input fields.

- Calculate Rankings: The application calculates the relative closeness to the ideal solution for each alternative and ranks them based on the TOPSIS scores.

- PDF Report: After ranking the alternatives, the application generates a PDF report showing the ranked alternatives.

- Email Results: Users can enter their email address and receive the PDF report as an attachment via email.

## Getting Started
1. Clone the repository to your local machine.
```
git clone https://github.com/yourusername/topsis-web-app.git
```
2. Install the required Python packages using pip.
```
pip install -r requirements.txt
```
3. Create a `config.ini` file in the project directory and provide your Gmail email and password as follows:
 ```
[login]
email = your_email@gmail.com
password = your_email_password
```
4. Run the application.
```
python app.py
```
5. Access the application in your web browser at http://localhost:5000 (5000 port might varies)

## Usage

1. Upload CSV File: Click on "Choose File" to select your CSV file and click "Upload" to load the decision matrix.

2. Weights Required: Enter Number of Weights Required. 

3. Enter Weights: Enter the weights for each criterion in the input fields and click "Submit" to start the TOPSIS calculation.

4. View Results: The application will display the ranked alternatives based on the TOPSIS scores. You can also download the PDF report showing the ranked alternatives.

5. Email Results: Enter your email address and click "Send Email" to receive the PDF report via email.

## Dependencies

- Flask
- Pandas
- NumPy
- ReportLab
- smtplib
  
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

