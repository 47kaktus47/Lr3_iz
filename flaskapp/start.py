print("Hello world")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
#наша новая функция сайта

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, RadioField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfYYBYbAAAAADJHJ8wKO4fzgq7uks6wuNL-sSnK'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfYYBYbAAAAALpp5LL3quMnXKXHAo2KdfQAm8-V'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
    
    cho=StringField('rotate', validators = [DataRequired()])
  
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])


 # поле формы с capture
    recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
    submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

## функция для оброботки изображения 
def draw(filename1,cho):
 ##открываем изображение 
 print(filename1)
 cho=int(cho)
 img= Image.open(filename1)

 
##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)

 plt.savefig(gr_path)
 plt.close()

 img= Image.open(filename1)
 for i in range(0,cho):
    a = img.crop((0, 0, int( y * 0.5), int(x * 0.5)))
    b = img.crop((int( y * 0.5), 0, y, int(x * 0.5)))
    c = img.crop((int( y * 0.5), int(x * 0.5), y, x))
    d = img.crop((0, int(x * 0.5), int( y * 0.5), x))
    img.paste(a, (0, int(y * 0.5)))
    img.paste(b, (int(x * 0.5), int(x * 0.5)))
    img.paste(c, (int(x * 0.5), 0))
    img.paste(d, (0, 0))
##сохраняем новое изображение


 print(img)
 #img = Image.fromarray(img)
 new_path = "./static/new.png"
 print(img)
 img.save(new_path)
 
 return new_path, gr_path  

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename1=None

 newfilename=None
 grname=None
 
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename1 = os.path.join('./static', secure_filename(form.upload.data.filename))


  cho=form.cho.data
  form.upload.data.save(filename1)

  newfilename, grname = draw(filename1,cho)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image1_name=newfilename,gr_name=grname, ishd1=filename1)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
