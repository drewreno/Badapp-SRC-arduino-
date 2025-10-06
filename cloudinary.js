const cloudinary = require('cloudinary').v2;
const fs = require('fs');
const path = require('path');

// Configure Cloudinary with your credentials
cloudinary.config({ 
  cloud_name: 'dsos2ijvk', 
  api_key: '357994591796565', 
  api_secret: 'JF3y6_QW-MW2HDCAPKsOtyqLLMg',
  secure: true
});

// Directory of the folder you want to upload
const directoryPath = path.join(__dirname, 'bmp_frames');

// Read files from the directory
fs.readdir(directoryPath, function (err, files) {
  if (err) {
    return console.log('Unable to scan directory: ' + err);
  } 

  files.forEach(function (file) {
    // Upload each file to Cloudinary
    cloudinary.uploader.upload(path.join(directoryPath, file), 
      { folder: "bmp" }, // Optional: specify a folder in Cloudinary
      function (error, result) {
        console.log(result, error);
      });
  });
});
