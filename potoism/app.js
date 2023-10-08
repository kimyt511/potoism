const express = require("express");
const path = require("path");
const multer = require("multer");
const fs = require("fs");
const { exec } = require("child_process");

const app = express();

try {
  fs.readdirSync("uploads");
} catch (error) {
  console.error("create uploads folder");
  fs.mkdirSync("uploads");
}
const storage = multer.memoryStorage();
const upload = multer({
  storage: storage,
  limit: { fileSize: 100 * 1024 * 1024 }
});
// const upload = multer({
//   storage: multer.diskStorage({
//     destination(req, file, done) {
//       done(null, "uploads/");
//     },
//     filename(req, file, done) {
//       console.log(req.body);
//       const ext = path.extname(file.originalname);
//       const filepath =
//         "uploads/" +
//         req.body["phone_number"] +
//         path.basename(file.fieldname, ext) +
//         ext;
//       done(
//         null,
//         req.body["phone_number"] + path.basename(file.fieldname, ext) + ext
//       );
//       // exec(
//       //   "sudo gsutil cp " + filepath + " gs://kimyt0511",
//       //   (error, stdout, stderr) => {
//       //     if (error) {
//       //       console.error(`exec error: ${error}`);
//       //       return;
//       //     }
//       //     console.log(`stdout: ${stdout}`);
//       //     console.error(`stderr: ${stderr}`);
//       //   }
//       // );
//     },
//   }),
//   limits: { fileSize: 100 * 1024 * 1024 },
// });

app.set("port", process.env.PORT || 80);
app.use(express.static(path.join(__dirname, "public")));
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/index.html"));
});
// app.post(
//   "/upload",
//   upload.fields([
//     { name: "phone_number" },
//     { name: "image1" },
//     { name: "image2" },
//     { name: "image3" },
//     { name: "image4" },
//   ]),
//   (req, res) => {
//     console.log(req.files, req.body);

//     // Check if all images are uploaded
//     if (
//       !req.files.image1 ||
//       !req.files.image2 ||
//       !req.files.image3 ||
//       !req.files.image4
//     ) {
//       return res.status(400).send("사진 4개를 모두 업로드 해주세요");
//     }
//     const validMimeTypes = [
//       "image/jpeg",
//       "image/png",
//       "image/gif",
//       "image/webp",
//       "image/bmp",
//       "image/tiff",
//     ];

//     for (let field in req.files) {
//       for (let uploadedFile of req.files[field]) {
//         if (!validMimeTypes.includes(uploadedFile.mimetype)) {
//           return res
//             .status(400)
//             .send(
//               "<script>alert('유효하지 않은 이미지 형식입니다.'); window.history.back();</script>"
//             );
//         }
//       }
//     }

//     //숫자 유효성 검사
//     const regex = /^[0-9]+$/;
//     if (!regex.test(req.body.phone_number)) {
//       return res
//         .status(400)
//         .send(
//           "<script>alert('숫자만 입력 가능합니다.'); window.history.back();</script>"
//         );
//     }

//     res.redirect("/");
//   }
// );

app.post("/uploadImage", upload.single("imageDataURL"), (req, res) => {
  if (!req.body.imageDataURL) {
    return res
      .status(400)
      .json({ message: "이미지 데이터가 전송되지 않았습니다." });
  }

  // 이미지 데이터를 FormData에서 가져옵니다.
  const imageDataURL = req.body.imageDataURL;
  const imageData = imageDataURL.split(",")[1];
  const imageBuffer = Buffer.from(imageData, "base64");

  // 이미지 처리 또는 저장 등 필요한 작업을 수행합니다.
  // 이 예제에서는 이미지를 public 폴더에 저장합니다. // base64 문자열을 Buffer로 변환
  const imageName = req.body.phone_number + ".jpg";

  // public 폴더에 이미지 저장
  fs.writeFileSync(`uploads/${imageName}`, imageBuffer);
  res.redirect("/");
  // res.json({ message: "이미지 업로드가 성공했습니다." });
});

app.listen(app.get("port"), () => {
  console.log(app.get("port"));
});
