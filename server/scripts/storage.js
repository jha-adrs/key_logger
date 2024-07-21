// manages storage

const awsSDK = require("@aws-sdk/client-s3");
//Skip for local file storage
const client = new awsSDK.S3Client({ 
    region: "ap-south-1",
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    } 
});
const saveFile = async (file, mac_address) => {
    try {
        // Save directly to local storage
        console.log("Creting file in local storage", mac_address , file.originalname);
        const folder = `${mac_address}`;
        
        const path = `${folder}/${file.originalname}-${new Date().getTime()}.txt`;
        if(!file.buffer){
            console.log("No buffer found in file");
            return null;
        }
        // fs.writeFile(path, file.buffer, (err) => {
        //     if (err) {
        //         console.error(err);
        //         return null;
        //     }
        //     console.log("File saved successfully");
        // });

        const command = new awsSDK.PutObjectCommand({
            Bucket: "testing-bucket-mng",
            Key: path,
            Body: file.buffer
        });
        const response = await client.send(command);
        console.log("File saved successfully", response);
        return {
            path,
            awsResponse: response
        };
    } catch (error) {
        console.error(error);
        return null;
    }
}

module.exports = {
    saveFile
}