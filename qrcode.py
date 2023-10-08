import qrcode

qrl = "34.64.118.3"
qr_gen = qrcode.make(qrl)
qr_gen.save("./download/qrcodeofSite.png")