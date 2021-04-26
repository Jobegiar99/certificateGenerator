from PIL import Image, ImageDraw, ImageFont
import pandas as pd 
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

userEmail = input("Ingresa el correo desde el cual vas a enviar los certificados:\n")
userPassw = input("Ingresa la contraseña de tu correo:\n")
userCSV   = input("Ingresa el nombre del archivo csv (debe de estar en el mismo directorio que este archivo):\n")
templateImage = input("Ingresa el nombre del archivo que sera utilizado como template junto con la extension (debe de ser una imagen):\n")
fontName = input("Ingresa el nombre del archivo que se utiliza para el font (debe de estar en el mismo directorio y tener extension .ttf):\n")
fontSize = input("Ingresa el tamaño que deberá tener el font del nombre:\n")
fontColor = input("Ingresa el color deseado para el font (puede ser rgb,rgba o hexadecimal):\n")
mailSubject = input("Ingresa el motivo por el cual se enviara el correo (ejemplo: Certificado por haber asistido al congreso):\n")

try:
    csv = pd.read_csv(userCSV)

except Exception as e:
    print("No se encontro el archivo.",e)

def generateCertificate():
    for index in range(len(csv)):
        try:
            #load data
            nombre = csv.iloc[index]['Nombre']
            apellidoPaterno = csv.iloc[index]['Apellido paterno']
            apellidoMaterno = csv.iloc[index]['Apellido materno']
            correo = csv.iloc[index]['Dirección de correo electrónico']
            nombreCompleto = nombre + " " + apellidoPaterno + " " + apellidoMaterno
            image = Image.open(templateImage)

            #prepare everything
            font = ImageFont.truetype(r""+fontName, size= fontSize )
            imageWidth = image.width
            imageHeight = image.height
            textWidth, textHeight = draw.textsize(nombreCompleto, font = fontName)
            (xNombre, yNombre) = ((W-w)/2, (H-h)/2)
            
            #add the text to the image
            draw.text( (xNombre, yNombre), nombreCompleto, fill = fontColor, font = font, stroke_fill = '#211A3F', stroke_width = 15)

            # save the edited image
            image.save(nombreCompleto + ".png")
            try:
                sendMail(nombreCompleto,correo)

            except Exception as e:
                print("No se pudo enviar el correo a:",nombreCompleto)
                print(e)

        except Exception as e:
            print("No se pudo generar el archivo con indice: ", str(index + 1))
            print(e)


def sendMail( name, email ):
    port = 465  # For SSL


    attachment = "./"+ name+ ".png"

    message = MIMEMultipart()
    message["Subject"] = mailSubject
    message["From"] = userEmail
    message["To"] = email

    msgText = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % ("", attachment), 'html')
    fp = open(attachment, 'rb')                                                    
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<{}>'.format(attachment))
    message.attach(img)


    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    html = """\
    <html>
    <body align = "center">
        <img width = 50% height = 50% src = "https://lh3.googleusercontent.com/yRGddEhLR8e-ioFew5OAO8PECQfQi2dfPbblKbrBuxWh1mJfyOzPSE0xmSNGjk_6_6poi-EW65IxWszs-LkZ42XeAarL-SjR4um_zZghoRyNerPvQSt-zORrgE-ExwhvBogHW2E-dN-p32Jqrh-P1OlcEjm_npTTU-OV395RX39eau25xkPhpxki45Gwv2W_6cerpk5ESZnAGvxiWRwcPDICoj3DrHb-TKMTQzcFnPaQvuOyEfeZeP8LG7qmAcLidIALoxN8m3nrEW96Llc91NnoL50WUm6YfKqffXK_4iAvOtCQOg3YVk_UYF9C1UOixJxN6yGkfJtRC25WtUbTJUukuAuayAPXMW58OUvWyg38Tit9gRe5lQ2OtX9lyE6IVGMSVwIOsxspbvqhG-txJ8uZvqcvXmjETDGJKGbDrBq_0B3twVolNs0NE1nvV03Py2IxIsBuGGT3EbAJKaw5mWHH0_BX3tbMf3ridfu7k3kJSpANsNHMuswT7esbZrPt0RzGkItjrRxEjpMX2l8zRsIXU0QW8YY7QzAbcDu3olpQpyIFfud-Vl3y_zCf5TifwleDFVlr3HotM7rr0goRaVGC_m0gxss5ANTAiqr6zO41kW7HIYqLOHi0lrGj4EN2utD-jln3JPO0Lx4s1_CqX8cwN_c6k53QFgAcJf5HhUcuTocrpCl_2thLUBe_XsoqF7PAKC53LG2lb-aE0iUoNxHS=w1600-h400-no?authuser=0">
            <br>
            <br>
        <p>Hola """ + name + """,
            <br><br>
                Este es un mensaje automatizado con el cual te enviamos tu certificado. 
            <br>
                Si llega a haber algun problema con la colocacion del nombre por favor envia un mensaje a la cuenta de<br>
                instagram de la saitc <a href = "https://www.instagram.com/saitc.mty/"> @saitc.mty </a><br>
            <br><br>
                Podrás acceder a las grabaciones por medio de <a href = "driveURL"> este enlace </a>, todavía se están procesando y subiendo.
            <br><br>
                Espero que hayas disfrutado de los talleres :) Sigue la cuenta oficial de la saitc para enterarte de más eventos
        </p>
    </body>
    </html>
    """

    htmlToAdd = MIMEText(html, "html")
    message.attach(htmlToAdd)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(userEmail, userPassw)

        server.sendmail(
            userEmail, email, message.as_string()
        )

generateCertificate()