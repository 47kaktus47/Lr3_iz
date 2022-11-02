print("Hello world")
import sys
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
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le2kPwcAAAAAAjXJ5YpKnaf1KfO3fLMjVsHDcTI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le2kPwcAAAAAAgnOBdJG2OEh_c2trx_8wb7AJ9O'
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
    
    cho=StringField('blend', validators = [DataRequired()])
  
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
    upload1 = FileField('Load image1', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    upload2 = FileField('Load image2', validators=[
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
def draw(filename1, filename2, cho):
 ##открываем изображение 
 print(filename1)
 sys.stdout.flush()
 cho=int(cho)
 img= Image.open(filename1)
 img2= Image.open(filename2)
 
##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path1 = "./static/newgr1.png"
 sns.displot(data)

 plt.savefig(gr_path1)
 plt.close()
 
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img2, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path2 = "./static/newgr2.png"
 sns.displot(data)
 
 plt.savefig(gr_path2)
 plt.close()

 img= Image.open(filename1)
 img= np.array(img.resize((224,224)))/255.0
 img = Image.fromarray((img * 255).astype(np.uint8))

 img2= Image.open(filename2)
 img2= np.array(img2.resize((224,224)))/255.0
 img2 = Image.fromarray((img2 * 255).astype(np.uint8))
 
 
 img3 = Image.blend(img1,img2,cho)
 
 
##сохраняем новое изображение


 print(img)
 #img = Image.fromarray(img)
 new_path = "./static/new.png"
 print(img)
 img.save(new_path)
 
 return new_path, gr_path1, gr_path2  

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename1=None
 filename2=None
 newfilename=None
 grname1=None
 grname2=None
 
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename1 = os.path.join('./static', secure_filename(form.upload1.data.filename))
  filename2 = os.path.join('./static', secure_filename(form.upload2.data.filename))
  ##filename1 = 'flaskapp\static\images.jpg'

  cho=form.cho.data
  form.upload.data.save(filename1)
  form.upload.data.save(filename2)

  newfilename, grname1, grname2 = draw(filename1,filename2,cho)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image1_name=newfilename,gr_name=grname1,gr_name2=grname2, ishd1=filename1, ishd2=filename2)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
