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
from wtforms import StringField, SubmitField, TextAreaField
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
 size1 = StringField('size1', validators = [DataRequired()])
 size2 = StringField('size2', validators = [DataRequired()])
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
def draw(filename,size1,size2):
 ##открываем изображение 
 print(filename)
 img= Image.open(filename)
 img2= Image.open(filename)
##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 #plt.show()
 plt.savefig(gr_path)
 plt.close()

##рисуем рамки
 size1=int(size1)
 size2=int(size2)
 height = 224
 width = 224
 img= np.array(img.resize((height,width)))/255.0
 print(size1)
 img[:size1,:,1] = 0
 img[:,0:size1,1] = 0
 img[:,224-size1:,1] = 0
 img[224-size1:,:,1] = 0

 img2= np.array(img2.resize((height,width)))/255.0
 print(size2)
 img2[:size2,:,1] = 0
 img2[:,0:size2,1] = 0
 img2[:,224-size2:,1] = 0
 img2[224-size2:,:,1] = 0
##сохраняем новое изображение
 img = Image.fromarray((img * 255).astype(np.uint8))
 img2 = Image.fromarray((img2 * 255).astype(np.uint8))
 print(img)
 #img = Image.fromarray(img)
 new_path1 = "./static/new1.png"
 print(img)
 img.save(new_path1)
 return new_path, gr_path, new_path1

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 newfilename1=None
 grname=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
 
  sz1=form.size1.data
  sz2=form.size2.data
  form.upload.data.save(filename)
  newfilename, grname, newfilename1 = draw(filename,sz1,sz2)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image1_name=newfilename,gr_name=grname,image2_name=newfilename1)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
