import pandas as pd
import pdfkit
import jinja2
from datetime import datetime
import inspect
from modules import app

'''
input: Fltered data from the database.
processing: converst the data into a HTML file and converts the html file to PDF.
Output: NONE
'''
def createPDF(data,columns):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ' \
        + ','.join(columns))
    df = pd.DataFrame(data, columns=columns)
    def color_negative_red(val):
        color = 'black'
        return f'color: {color}'

    styler = df.style.applymap(color_negative_red)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template('myreport.html')
    html = template.render(my_table=styler.render())

    with open('report.html', 'w') as f:
        f.write(html)
    pdfkit.from_file('report.html', 'report.pdf')
