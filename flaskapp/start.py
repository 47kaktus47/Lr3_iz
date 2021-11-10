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
    cho = RadioField('what to do', coerce=int, choices=[(0, 'umnozh'),(1, 'obrat'),(2,'umn na kf')])
    kfr=StringField('kf for r', validators = [DataRequired()])
    kfg=StringField('kf for g', validators = [DataRequired()])
    kfb=StringField('kf for b', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
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
def draw(filename1,filename2,cho,kfr,kfg,kfb):
 ##открываем изображение 
 print(filename1)
 cho=int(cho)
 kfr=int(kfr)
 kfg=int(kfg)
 kfb=int(kfb)

 img= Image.open(filename1)
 img1=Image.open(filename2)
 
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


 height = 224
 width = 224
 img= np.array(img.resize((height,width)))/255.0
 from numpy.linalg import inv
 height = 224
 width = 224
 img1= np.array(img1.resize((height,width)))/255.0
 if cho==0:
    img[:,:,0]=np.dot(img[:,:,0],img1[:,:,0])
    img[:,:,1]=np.dot(img[:,:,1],img1[:,:,1])
    img[:,:,2]=np.dot(img[:,:,2],img1[:,:,2])
 if cho==1:
    img[:,:,0]=inv(img[:,:,0])
    img[:,:,1]=inv(img[:,:,1])
    img[:,:,2]=inv(img[:,:,2])
 if cho==2:
    img[:,:,0]=img[:,:,0]*kfr
    img[:,:,1]=img[:,:,1]*kfg
    img[:,:,2]=img[:,:,2]*kfb
##сохраняем новое изображение
 img = Image.fromarray((img * 255).astype(np.uint8))

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
 filename2=None
 newfilename=None
 grname=None
 
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename1 = os.path.join('./static', secure_filename(form.upload.data.filename))
  filename2 = os.path.join('./static', secure_filename(form.upload2.data.filename))
  kfr=form.kfr.data
  kfg=form.kfg.data
  kfb=form.kfb.data
  cho=form.cho.data
  form.upload.data.save(filename1)
  form.upload2.data.save(filename2)
  newfilename, grname = draw(filename1,filename2,cho,kfr,kfg,kfb)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image1_name=newfilename,gr_name=grname, ishd1=filename1, ishd2=filename2)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
